from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

BOT_TOKEN = "7841263367:AAFhsbbzuxfvrMekdQ19rqMojiZuQxTHrho"  
CHAT_ID = "6473655119"  

# Menu Items categorized with prices
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

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create keyboard in rows of 2 for better visibility
    keyboard = []
    row = []
    for section in menu_sections.keys():
        row.append(InlineKeyboardButton(section, callback_data=section))
        if len(row) == 2:  # Change this value to adjust how many buttons per row
            keyboard.append(row)
            row = []
    if row:  # Add any remaining buttons as the last row
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select a menu section:", reply_markup=reply_markup)


# Handle section selection
async def section_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    section = query.data
    items = menu_sections[section]

    # Show items with prices in the selected section, each item on a new line
    keyboard = [[InlineKeyboardButton(f"{item} (₹{price})", callback_data=item)] for item, price in items.items()]  
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"You selected: {section}. Please choose an item:", reply_markup=reply_markup)


# Handle item selection
async def item_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    item = query.data
    price = None

    for section, items in menu_sections.items():
        if item in items:
            price = items[item]
            break

    context.user_data['order'] = context.user_data.get('order', [])
    context.user_data['order'].append((item, price))

    order_summary = "\n".join([f"{itm} (₹{prc})" for itm, prc in context.user_data['order']])
    await query.edit_message_text(f"Item added: {item} (₹{price})\nCurrent Order:\n{order_summary}\nType /confirm to place the order or /start to choose another section.")

# Confirm Order
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'order' in context.user_data and context.user_data['order']:
        order_summary = "\n".join([f"{item} (₹{price})" for item, price in context.user_data['order']])
        total_price = sum([price for _, price in context.user_data['order']])
        
        await update.message.reply_text(f"Order confirmed:\n{order_summary}\nTotal Price: ₹{total_price}")

        cafe_chat_id = CHAT_ID
        try:
            await context.bot.send_message(cafe_chat_id, f"New Order:\n{order_summary}\nTotal Price: ₹{total_price}")
        except Exception as e:
            await update.message.reply_text(f"Error sending message to cafe: {str(e)}")
    else:
        await update.message.reply_text("No items in your order. Type /start to start ordering.")

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(section_selection, pattern='|'.join(menu_sections.keys())))
    application.add_handler(CallbackQueryHandler(item_selection, pattern='|'.join([item for section in menu_sections.values() for item in section.keys()])))
    application.add_handler(CommandHandler("confirm", confirm_order))

    await application.initialize()
    await application.start()
    print("Bot is running...")

    await application.updater.start_polling()
    
    # Keep the bot running until interrupted
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
