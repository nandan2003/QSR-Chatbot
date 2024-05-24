import os
import streamlit as st
import openai
import speech_recognition as sr
from langchain.chains import LLMChain, SequentialChain
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.memory import ConversationBufferMemory
from constants import openai_key

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = openai_key

# Custom restaurant data
menu = {
    "Burgers": {"Cheeseburger": 5.00, "Veggie Burger": 4.50},
    "Pizzas": {"Margherita": 7.00, "Pepperoni": 8.50},
    "Drinks": {"Cola": 1.50, "Lemonade": 2.00},
    "Desserts": {"Ice Cream": 3.00, "Cake": 3.50}
}

# Initialize Streamlit
st.title("QSR Chatbot")

# Initialize the language model (llm)
llm = OpenAI(openai_api_key=openai_key)

# Define prompt templates
menu_prompt = PromptTemplate(
    input_variables=['query'],
    template="Show me the menu"
)

order_prompt = PromptTemplate(
    input_variables=['query'],
    template="Place an order for {query}"
)

cart_prompt = PromptTemplate(
    input_variables=['query'],
    template="Show the items in the cart"
)

# Define memory buffers
menu_memory = ConversationBufferMemory(input_key='query', memory_key='menu_history')
order_memory = ConversationBufferMemory(input_key='query', memory_key='order_history')
cart_memory = ConversationBufferMemory(input_key='query', memory_key='cart_history')

# Initialize LLM chains
menu_chain = LLMChain(llm=llm, prompt=menu_prompt, verbose=True, output_key='menu_response', memory=menu_memory)
order_chain = LLMChain(llm=llm, prompt=order_prompt, verbose=True, output_key='order_response', memory=order_memory)
cart_chain = LLMChain(llm=llm, prompt=cart_prompt, verbose=True, output_key='cart_response', memory=cart_memory)

# Sequential chain to handle different types of queries
qsr_chain = SequentialChain(
    chains=[menu_chain, order_chain, cart_chain],
    input_variables=['query'],
    output_variables=['menu_response', 'order_response', 'cart_response'],
    verbose=True
)

# Function to process the custom menu
def get_menu_response():
    response = "Here's our menu:\n"
    for category, items in menu.items():
        response += f"{category}:\n"
        for item, price in items.items():
            response += f"  - {item}: ${price:.2f}\n"
    return response

# Function to handle voice input
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.write(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I did not understand the audio.")
    except sr.RequestError:
        st.write("Could not request results; check your network connection.")
    return ""

# Initialize session state for conversation history and cart
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "cart" not in st.session_state:
    st.session_state.cart = []

# User input (text or voice)
st.write("Enter your query or click the button to use voice input:")
user_input = st.text_input("You: ", "")

if st.button("Use Voice Input"):
    user_input = get_voice_input()

# Display conversation history
if st.session_state.conversation_history:
    for message in st.session_state.conversation_history:
        st.write(message)

# Process user input
if user_input:
    st.session_state.conversation_history.append(f"You: {user_input}")

    # Custom response handling based on user input
    if "menu" in user_input.lower():
        chatbot_response = get_menu_response()
    elif "add" in user_input.lower() and "cart" in user_input.lower():
        item_to_add = user_input.lower().replace("add", "").replace("to cart", "").strip()
        added = False
        for category, items in menu.items():
            if item_to_add in items:
                st.session_state.cart.append((item_to_add, items[item_to_add]))
                chatbot_response = f"Added {item_to_add} to your cart."
                added = True
                break
        if not added:
            chatbot_response = "Item not found in the menu."
    elif "show" in user_input.lower() and "cart" in user_input.lower():
        if st.session_state.cart:
            cart_response = "Items in your cart:\n"
            total_cost = 0.0
            for item, price in st.session_state.cart:
                cart_response += f"  - {item}: ${price:.2f}\n"
                total_cost += price
            cart_response += f"Total cost: ${total_cost:.2f}"
            chatbot_response = cart_response
        else:
            chatbot_response = "Your cart is empty."
    elif "clear" in user_input.lower() and "cart" in user_input.lower():
        st.session_state.cart = []
        chatbot_response = "Cart cleared."
    elif "checkout" in user_input.lower():
        if st.session_state.cart:
            cart_response = "You are about to checkout with the following items:\n"
            total_cost = 0.0
            for item, price in st.session_state.cart:
                cart_response += f"  - {item}: ${price:.2f}\n"
                total_cost += price
            cart_response += f"Total cost: ${total_cost:.2f}"
            cart_response += "\nWould you like to add more items before checking out?"
            chatbot_response = cart_response
        else:
            chatbot_response = "Your cart is empty. Add items to your cart before checking out."
    elif "yes" in user_input.lower() and "checkout" in user_input.lower():
        chatbot_response = "Please add the items you want to your cart."
    elif "no" in user_input.lower() and "checkout" in user_input.lower():
        if st.session_state.cart:
            chatbot_response = "Proceeding to checkout. Thank you for your order!"
            st.session_state.cart = []  # Clear the cart after checkout
        else:
            chatbot_response = "Your cart is empty."
    else:
        # Get response from the sequential chain
        chatbot_response = qsr_chain.run(query=user_input)
    
    st.session_state.conversation_history.append(f"Bot: {chatbot_response}")

    # Clear input field
    user_input = ""

# Display current conversation
for message in st.session_state.conversation_history:
    st.write(message)
