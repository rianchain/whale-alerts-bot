from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# function when the user uses the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello to the new bot for whale alerts!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")


def main():
    bot_token = "7618502843:AAGFj67PXpCmE18PpCvF86CnyRsa4u9JYOQ"

    #create the application
    application = Application.builder().token(bot_token).build()

    # add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, echo))

    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    main()