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
        "Oreo Milkshake": 50
    },
    "Pizza": {
        "Margherita Pizza": 100,
        "Chicken Pizza": 150
    },
    "Rolls": {
        "Chicken Roll": 90,
        "Paneer Roll": 90
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