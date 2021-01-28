from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from lib.scrapping import getProductData, checkID

TYPING_CHECK, TYPING_ADD, CHOOSING_REM = range(3)

def start_cmd(update, context):
    # mensaje bienvenida
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="start"
        )

def check_cmd(update, context):
    # Request product url
    update.message.reply_text(
        text="Enter the product ID (i.e. product/<b>XXXXXX</b>)",
        parse_mode="HTML"
    )
    return TYPING_CHECK

def add_cmd(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="add"
    )
    return TYPING_ADD

# def remove_cmd(update, context):
#     context.bot.send_message(
#         chat_id=update.effective_chat.id, 
#         text="remove"
#     )
#     return CHOOSING_REM

# def list_cmd(update, context):
#     context.bot.send_message(
#         chat_id=update.effective_chat.id, 
#         text="list"
#     )
#     return TYPING_REPLY

def received_add(update, context):
    text = update.message.text


# comprobar si hay 10 no añadir más enlaces, máx 10 por usuario array database
    print(text)
    return ConversationHandler.END

def received_check(update, context):
    ID = update.message.text

    # Check url
    result = checkID(ID)
    text = ""

    if result == 0:
        data = getProductData(ID)
        text = "title: {name}".format(data['title'])
    else:
        text = "incorrect ID"
    # Get product data

    # Send data
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text
    )

    return ConversationHandler.END

if __name__ == "__main__":

    # Create the Updater
    updater = Updater(token='1560578141:AAHxpwm7uK0bwaicch4y-HNUD7ddWGtHzRE', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states TYPING REPLY
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('check', check_cmd),
            CommandHandler('add', add_cmd),
            # CommandHandler('remove', remove_cmd),
            # CommandHandler('list', list_cmd),
        ],
        states={
            TYPING_ADD: [MessageHandler(Filters.text, received_add)],
            TYPING_CHECK: [MessageHandler(Filters.text, received_check)],
            # CHOOSING_REM: [MessageHandler(Filters.text, received_information)],
        },
        fallbacks=[],
        # fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    