import streamlit as st
import openai
from langchain.chains import ConversationChain
from langchain.llms import OpenAI

# Set up OpenAI API key
openai.api_key = "your-openai-api-key"

# Initialize Streamlit
st.title("QSR Chatbot")

# Initialize the language model (llm)
llm = OpenAI(openai_api_key=openai.api_key)

# Initialize conversation chain with the language model
conversation = ConversationChain(llm=llm)

# Function to get response from OpenAI
def get_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.9,
    )
    return response.choices[0].text.strip()

# User input
user_input = st.text_input("You: ", "")

# Initialize session state for conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Display conversation history
if st.session_state.conversation_history:
    for message in st.session_state.conversation_history:
        st.write(message)

# Process user input
if user_input:
    st.session_state.conversation_history.append(f"You: {user_input}")

    # Get response from the conversation chain
    chatbot_response = conversation.run(user_input)
    st.session_state.conversation_history.append(f"Bot: {chatbot_response}")

    # Clear input field
    user_input = ""

# Display current conversation
for message in st.session_state.conversation_history:
    st.write(message)
