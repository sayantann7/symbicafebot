## Telegram Bot for SymbiCafe

This project implements a Telegram bot for SymbiCafe. Users can interact with the bot to select menu sections, choose items with prices, and place their order. The order is sent to the cafe via a Telegram message.

### Features

- Menu sections categorized by types (e.g., Milkshakes, Pizza, Rolls).
- Each menu section contains a list of items with prices.
- Users can select items, add them to their order, and confirm the order.
- Order summary with total price is displayed.
- The confirmed order is sent to a specified chat ID (cafe staff).

### Requirements

- Python 3.7+
- `python-telegram-bot` library
- Telegram Bot Token and Chat ID

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repository/telegram-menu-bot.git
   cd telegram-menu-bot
   ```

2. Install the required dependencies:

   ```bash
   pip install python-telegram-bot==20.0a0
   ```

3. Replace the following in the code:

   - `BOT_TOKEN`: Your Telegram bot token from the [BotFather](https://core.telegram.org/bots#botfather).
   - `CHAT_ID`: Chat ID where the confirmed order will be sent (cafe staff's chat or group).

4. Run the bot:

   ```bash
   python bot.py
   ```

### Usage

1. Start the bot by typing `/start` in the Telegram chat with the bot.
2. Choose a menu section (e.g., "Pizza", "Rolls").
3. Select an item from the section. It will be added to your order.
4. To confirm the order, type `/confirm`.

### Bot Commands

- **/start**: Start the bot and view the menu sections.
- **/confirm**: Confirm the current order and send it to the cafe.

### Code Overview

#### Menu Sections

```python
menu_sections = {
    "Milkshakes": {
        "Tea": 30,
        "Hot Coffee": 40,
        "Cold Coffee": 40,
        "Citrus Blue Soda": 40,
        "Lemon Pudina Soda": 40,
        "Oreo Milkshake": 50
    },
    "Finger Chips": {
        "Finger Chips": 70,
        "Peri Peri Finger Chips": 80
    },
    "Burger": {
        "Veg Burger": 65,
        "Veg Cheese Burger": 80,
        "Veg Noodles Burger": 80,
        "Chicken Burger": 100,
        "Chicken Noodles Burger with Cheese": 120
    },
    "Pizza": {
        "Margherita Pizza": 100,
        "Chicken Pizza": 150
    },
    "Momos": {
        "Veg Steam Momo": 70,
        "Veg Fry Momo": 80,
        "Chicken Steam Momo": 80,
        "Chicken Fry Momo": 90
    },
    "Rolls": {
        "Egg Roll": 70,
        "Veg Noodles Roll": 75,
        "Paneer Roll": 90,
        "Chicken Roll": 90,
        "Paneer Tikka Roll": 90,
        "Chicken Tikka Roll": 100
    },
    "Chicken Snacks": {
        "Chicken Manchurian Dry": 140,
        "Chicken Manchurian Gravy": 160,
        "Chicken 65 Dry": 140,
        "Chicken 65 Gravy": 160,
        "Chicken Lollipop Fry": 190,
        "Chicken Lollipop Masala": 200
    },
    "Veg Rice": {
        "Veg Fried Rice": 110,
        "Veg Schezwan Rice": 130,
        "Veg Shanghai Rice": 130,
        "Veg Manchurian Rice": 150,
        "Veg Triple Rice": 150,
        "Paneer Triple Rice": 170,
    },
    "Chicken Rice": {
        "Egg Fried Rice": 130,
        "Chicken Fried Rice": 130,
        "Chicken Combination Rice": 110,
        "Chicken Shanghai Rice": 140,
        "Chicken Schezwan Rice": 140,
        "Chicken Triple Rice": 160,
        "Chicken Manchurian Rice": 160
    },
    "Veg Noodles": {
        "Veg Hakka Noodles": 120,
        "Veg Schezwan Noodles": 130,
        "Veg Manchurian Noodles": 150
    },
    "Chicken Noodles": {
        "Egg Hakka Noodles": 145,
        "Chicken Hakka Noodles": 145,
        "Chicken Schezwan Noodles": 150,
        "Chicken Manchurian Noodles": 160,
        "Chicken Triple Noodles": 160
    }
}
```

#### Bot Functionality

1. **Start Command** (`/start`): Displays all available menu sections using inline keyboard buttons. Each section button leads to a list of items in that section.
2. **Section Selection**: Once a section is selected, the bot displays items with prices for that section, each on a new line.
3. **Item Selection**: Adds the selected item to the user's current order and displays the updated order summary.
4. **Confirm Order** (`/confirm`): Sends the order summary and total price to the user and the specified cafe chat.

#### Main Functions

- `start()`: Displays the main menu sections.
- `section_selection()`: Handles the user's section choice and displays available items in that section.
- `item_selection()`: Handles item selection and updates the order summary.
- `confirm_order()`: Confirms the order and sends it to the cafe.

### Customization

- **Menu Sections**: You can modify `menu_sections` to add, remove, or edit categories and items.
- **Keyboard Layout**: Adjust the number of buttons per row by modifying the line:

  ```python
  if len(row) == 2:  # Change to control number of buttons per row
  ```

### Error Handling

If an error occurs while sending the message to the cafe, the bot will display an error message to the user. You can also handle additional errors based on your use case.