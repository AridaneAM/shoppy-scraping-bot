from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

TOKEN = "1560578141:AAHxpwm7uK0bwaicch4y-HNUD7ddWGtHzRE"

NAME, DOG_SAVE = range(2)

def start(update, context):
    update.message.reply_text(
        'send /name to activate save a dog name'
    )
    return NAME

def name(update, context):
    update.message.reply_text('What do you want to name this dog?')

    return DOG_SAVE

def dog_save(update, context):
    name = update.message.text
    update.message.reply_text(f'Dog saved as {name}')

    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        fallbacks=[],

        states={
            NAME: [CommandHandler('name', name)],
            DOG_SAVE: [MessageHandler(Filters.text, dog_save)],
        },
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()