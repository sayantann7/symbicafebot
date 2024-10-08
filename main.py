from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import random
import asyncio
import os

BOT_TOKEN = os.getenv('BOT_TOKEN_ID') 
CHAT_ID =  os.getenv('CAFE_CHAT_ID')

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

hostel_list = ["Hostel A", "Hostel B", "Hostel C", "Hostel D", "Hostel E", "Hostel F", "Hostel G", "Hostel H"]

# Choose hostel first
async def choose_hostel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(hostel, callback_data=hostel)] for hostel in hostel_list]  # Each hostel in a new row
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select your hostel:", reply_markup=reply_markup)

# Handle hostel selection
async def hostel_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data['hostel'] = query.data
    await query.edit_message_text(f"Hostel selected: {query.data}. You can now start your order by typing /order.")

# Asking for the phone number
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter your phone number:")

# Handle phone number input
async def handle_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.message.text

    # Validate if the phone number is a valid number (basic check)
    if not phone_number.isdigit() or len(phone_number) < 10:
        await update.message.reply_text("Invalid phone number. Please enter a valid 10-digit number.")
        return
    
    # Store phone number in user data
    context.user_data['phone_number'] = phone_number
    await update.message.reply_text(f"Thanks for sharing your phone number: {phone_number}")
    await choose_hostel(update, context)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button click

    # Check if the callback_data matches "start_order"
    if query.data == "start_order":
        await query.message.reply_text("Starting your order...")
        # Now trigger the /order command
        await order(update, context)

# Ordering: Moved from /start to /order
async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the phone number has been provided
    if 'phone_number' not in context.user_data:
        await update.message.reply_text("Please provide your phone number first using /start.")
        return

    # Check if the hostel has been selected
    if 'hostel' not in context.user_data:
        await update.message.reply_text("Please select your hostel first.")
        return

    # Continue with the ordering process
    keyboard = []
    row = []
    for section in menu_sections.keys():
        row.append(InlineKeyboardButton(section, callback_data=section))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
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
    keyboard = []
    keyboard.append([InlineKeyboardButton(section, callback_data=section)])
    for item, price in items.items():
        keyboard.append([InlineKeyboardButton(f"{item} (₹{price})", callback_data=item)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"You selected: {section}. Please choose an item:", reply_markup=reply_markup)

# Handle item selection (Add to order)
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
    await query.edit_message_text(f"Item added: {item} (₹{price})\nCurrent Order:\n{order_summary}\nType /confirm to place the order, /remove_item to remove items, or /order to choose another section.")

# Handle removing an item from the order
async def remove_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'order' in context.user_data and context.user_data['order']:
        # Display the current items to remove
        keyboard = [[InlineKeyboardButton(f"{item} (₹{price})", callback_data=f"remove_{item}")] for item, price in context.user_data['order']]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Select an item to remove:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Your order is empty. Type /order to add items.")

# Handle item removal
async def item_removal_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    item_to_remove = query.data.replace("remove_", "")  # Extract the item name
    context.user_data['order'] = [(item, price) for item, price in context.user_data['order'] if item != item_to_remove]

    order_summary = "\n".join([f"{itm} (₹{prc})" for itm, prc in context.user_data['order']])
    await query.edit_message_text(f"Item removed: {item_to_remove}\nCurrent Order:\n{order_summary}\nType /confirm to place the order, or /order to add more items.")

# Edit hostel selection (if students want to change their hostel)
async def edit_hostel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await choose_hostel(update, context)

# Confirm Order with hostel and order ID
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if phone number is provided
    if 'phone_number' not in context.user_data:
        contact_button = InlineKeyboardButton(text="Share your phone number", request_contact=True)
        reply_markup = InlineKeyboardMarkup([[contact_button]], one_time_keyboard=True)
        await update.message.reply_text("Please share your phone number before confirming the order.", reply_markup=reply_markup)
        return

    # Check if order exists
    if 'order' in context.user_data and context.user_data['order']:
        hostel = context.user_data.get('hostel', "No hostel selected")
        phone_number = context.user_data.get('phone_number', "No phone number")
        order_summary = "\n".join([f"{item} (₹{price})" for item, price in context.user_data['order']])
        total_price = sum([price for _, price in context.user_data['order']])
        order_id = random.randint(100000, 999999)

        await update.message.reply_text(f"Order confirmed:\nHostel: {hostel}\nPhone: {phone_number}\nOrder ID: {order_id}\n{order_summary}\nTotal Price: ₹{total_price}")

        # Send order to cafe
        cafe_chat_id = CHAT_ID
        try:
            await context.bot.send_message(cafe_chat_id, f"New Order:\nHostel: {hostel}\nPhone: {phone_number}\nOrder ID: {order_id}\n{order_summary}\nTotal Price: ₹{total_price}")
        except Exception as e:
            await update.message.reply_text(f"Error sending message to cafe: {str(e)}")
        
        # Clear the order after confirmation
        context.user_data['order'] = []  # Reset order so user can place a new one
    else:
        await update.message.reply_text("No items in your order. Type /order to start ordering.")

# Get chat ID and reply to the user
async def getchatid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your chat ID is: {update.effective_chat.id}")

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone_number))  # Handles the phone number input
    application.add_handler(CommandHandler("order", order))
    application.add_handler(CommandHandler("confirm", confirm_order))
    application.add_handler(CommandHandler("remove_item", remove_item))
    application.add_handler(CommandHandler("edit_hostel", edit_hostel))
    application.add_handler(CommandHandler("getchatid", getchatid))

    # Callback query handlers
    application.add_handler(CallbackQueryHandler(section_selection, pattern='|'.join(menu_sections.keys())))
    application.add_handler(CallbackQueryHandler(item_selection, pattern='|'.join([item for section in menu_sections.values() for item in section.keys()])))
    application.add_handler(CallbackQueryHandler(item_removal_selection, pattern=r'^remove_.*'))
    application.add_handler(CallbackQueryHandler(hostel_selection, pattern='|'.join(hostel_list)))
    application.add_handler(CallbackQueryHandler(button_click))

    await application.initialize()
    await application.start()
    print("Bot is running...")

    await application.updater.start_polling()
    
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())