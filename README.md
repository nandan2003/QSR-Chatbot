# QSR-Chatbot

### How the QSR Chatbot Works

#### Conversation Flow

1. **Greeting and Menu Inquiry**:
   - **User Input**: The user can start by asking for the menu or a specific item.
   - **Bot Response**: The bot greets the user and provides the menu, listing categories like Burgers, Pizzas, Drinks, and Desserts with their respective items and prices.

2. **Adding Items to Cart**:
   - **User Input**: The user can request to add an item to their cart by mentioning the item name.
   - **Bot Response**: The bot confirms the addition of the specified item to the cart and updates the cart state.

3. **Viewing Cart**:
   - **User Input**: The user can ask to view the items in their cart.
   - **Bot Response**: The bot lists all the items currently in the cart along with their prices and the total cost.

4. **Clearing Cart**:
   - **User Input**: The user can request to clear their cart.
   - **Bot Response**: The bot clears the cart and confirms that the cart has been emptied.

5. **Checkout Process**:
   - **User Input**: The user can initiate the checkout process by requesting to checkout.
   - **Bot Response**: The bot displays the items in the cart with the total cost and asks the user if they want to add more items before proceeding to checkout.
     - **If the user wants to add more items**: The bot prompts the user to specify the items they wish to add.
     - **If the user does not want to add more items**: The bot proceeds to checkout, thanks the user for their order, and clears the cart.

#### Types of Responses

1. **Menu Response**:
   - Provides a detailed list of menu items and their prices.
   - Example: "Here's our menu: Burgers - Cheeseburger: $5.00, Veggie Burger: $4.50..."

2. **Order Confirmation**:
   - Confirms the addition of items to the cart.
   - Example: "Added Cheeseburger to your cart."

3. **Cart Summary**:
   - Lists the items in the cart along with individual prices and the total cost.
   - Example: "Items in your cart: Cheeseburger: $5.00, Cola: $1.50. Total cost: $6.50."

4. **Cart Clearing Confirmation**:
   - Confirms that the cart has been cleared.
   - Example: "Cart cleared."

5. **Checkout Initiation**:
   - Displays the items in the cart, the total cost, and asks if the user wants to add more items.
   - Example: "You are about to checkout with the following items: Cheeseburger: $5.00, Cola: $1.50. Total cost: $6.50. Would you like to add more items before checking out?"

6. **Final Checkout Confirmation**:
   - Confirms the completion of the checkout process and thanks the user.
   - Example: "Proceeding to checkout. Thank you for your order!"

#### Workflow

1. **User Input Processing**:
   - The bot captures user input via text or voice.
   - It identifies the type of query (menu request, add to cart, view cart, clear cart, checkout).

2. **Menu Handling**:
   - When the user asks for the menu, the bot retrieves the menu items and responds with a detailed list.

3. **Cart Management**:
   - When the user adds an item, the bot updates the cart state and confirms the addition.
   - When the user requests to view the cart, the bot retrieves the current cart state and displays the items.

4. **Checkout Process**:
   - When the user initiates checkout, the bot provides a summary of the cart and asks if they want to add more items.
   - Based on the user's response, the bot either prompts for more items or proceeds to checkout, clearing the cart after confirmation.

5. **Memory Management**:
   - The bot uses session state to maintain the conversation history and cart items across multiple interactions.

This comprehensive workflow ensures a smooth and interactive customer experience, covering all necessary steps from menu browsing to checkout.
