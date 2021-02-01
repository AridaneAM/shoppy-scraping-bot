import os
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from telegram import ReplyKeyboardMarkup
from lib.scrapping import getProductData
from lib.database import Database


# Database instance
global db

# Bot user states
TYPING_CHECK, TYPING_ADD, CHOOSING_REM = range(3)

def start_cmd(update, context):
    # Register user if not already
    db.insertUser(int(update.effective_chat.id))

    # mensaje bienvenida
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        parse_mode='MarkdownV2',
        text="✋ Welcome to the Shoppy alert bot\! ✋\n\n"
        "📋 **The following commands are available:** 📋\n"
        "🔸 /add: Add a new product URL for its notification\.\n"
        "🔸 /remove: Remove a registered product URL\.\n"
        "🔸 /check: Get the current shoppy product stock\.\n"
        "🔸 /list: View the list of registered URLs\.\n"
        )
    return ConversationHandler.END

def check_cmd(update, context):
    # Request product url
    update.message.reply_text(
        text="Enter the product ID (i.e. product/<b>XXXXXX</b>)",
        parse_mode="HTML"
    )
    return TYPING_CHECK

def add_cmd(update, context):
    # Request product url
    update.message.reply_text(
        text="Enter the product ID (i.e. product/<b>XXXXXX</b>)",
        parse_mode="HTML"
    )
    return TYPING_ADD

def remove_cmd(update, context):
    products = db.fetchUserProducts(int(update.effective_chat.id))
    reply_keyboard =[]

    if len(products) == 0:
        text = "⚠️ You don't have products registered."
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=text
        )
        return ConversationHandler.END
    else:
        for product in products:
            reply_keyboard.append([product[0]])

        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Select the product you want to remove:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, 
            one_time_keyboard=True)
        )
        return CHOOSING_REM

def list_cmd(update, context):
    products = db.fetchUserProducts(int(update.effective_chat.id))

    if len(products) == 0:
        text = "⚠️ You don't have products registered."
    else:
        text = "ℹ️ You have the following products registered:\n"
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=text,
            disable_web_page_preview=True
        )
        text = ""
        for product in products:
            text += ("🔹 {title}\n\r🔗" +
            "https://shoppy.gg/product/{product}\n\n").format(product=product[0], title=product[1])

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text,
        disable_web_page_preview=True
    )
    return ConversationHandler.END

def received_add(update, context):
    product = update.message.text

    # Scrapping product data
    result = getProductData(product)
    text = ""

    # Check ID
    if result['title'] == '0':
        text = "incorrect product ID"
    else:
        # Check n of saved IDs in db(max:5)
        nProducts = len(db.fetchUserProducts(int(update.effective_chat.id)))

        if nProducts < 5:
            # Save ID
            result = db.insertNotification(int(update.effective_chat.id), 
                product, result['title'], result['stock'])
            if result == 0:
                # Format message
                text = "✅ Product added to the notification list successfully"                
            else:
                # Format message
                text = "⚠️ The product is already in the notification list"     
        else:
            # Format error message
            text = ("⚠️ You have exceeded the limit of products notification (5), "
                "remove an ID before adding another one.")

    # Send telegram message
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text
    )
    return ConversationHandler.END

def received_check(update, context):
    ID = update.message.text

    # Scrapping product data
    result = getProductData(ID)

    # Format message
    text = ""
    if result['title'] == '0':
        text = "incorrect product ID"
    else:
        text = """ℹ️ Product: {title}
        \n\r💸 Price: {price}
        \n\r📉 Stock: {stock}
        """.format(
                title=result['title'],
                price=result['price'],
                stock=result['stock'])

    # Send telegram message
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text
    )
    return ConversationHandler.END

def received_remove(update, context):
    product = update.message.text
    result = db.removeNotification(int(update.effective_chat.id), product)
    text = ""

    if result == 0:
        text = "✅ Product removed from the notification list successfully"                
    else:
        text = "🛑 Error while removing the notification"                

    # Send telegram message
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text
    )
    return ConversationHandler.END

def notify_stock(context):
    print("Periodic task (check stock)")
    # Get list of products
    result = db.fetchAllProducts()
    products_dict = {}
    for row in result:
        if row[1] not in products_dict:
            products_dict[row[1]] = [[],[]]
            products_dict[row[1]][1]= row[2]
        products_dict[row[1]][0].append(row[0])
    print("product_dict:")
    print(products_dict)
    # Check stock for each product
    for product in products_dict:
        print("checking:" + str(product))
        result = getProductData(product)
        old_stock = products_dict[product][1]
        new_stock = result['stock']
        new_title = result['title']
        print("old stock: " + str(old_stock))
        print("new stock: " + str(new_stock))
        print("new title: " + str(new_title))

        if new_stock > 0 and old_stock == 0:
            print("UPDATEING NEW STOCK")
            # update new stock
            db.updateStock(product, new_stock, new_title)
            # send notification for each user
            for chat_id in products_dict[product][0]:
                print("SENDING TO: " + str(chat_id))
                text = """
                ❗️ New stock ❗️
                \n\rℹ️ {title}
                \n\r🔗 Link: https://shoppy.gg/product/{product}
                """.format(title = new_title, product=product)

                context.bot.send_message(
                    chat_id=chat_id, 
                    text=text,
                    disable_web_page_preview=True
                )

def periodic_task(context):
    # Remove products that are not longer registered for notificating
    db.removeProducts()
    # Check products and notify new stock
    notify_stock(context)


if __name__ == "__main__":
    # Create and init Database connection
    db = Database()

    # Create the Updater
    updater = Updater(token=os.environ['TOKEN'], use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states TYPING REPLY
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_cmd),
            CommandHandler('check', check_cmd),
            CommandHandler('add', add_cmd),
            CommandHandler('list', list_cmd),
            CommandHandler('remove', remove_cmd),
        ],
        states={
            TYPING_ADD: [MessageHandler(Filters.text, received_add)],
            TYPING_CHECK: [MessageHandler(Filters.text, received_check)],
            CHOOSING_REM: [MessageHandler(Filters.text, received_remove)],
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    # Add periodic job
    job_queue = updater.job_queue
    job_queue.run_repeating(periodic_task, interval= 300.0, first=30.0)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
