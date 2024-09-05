from telegram import Update
from telegram.ext import Application, CommandHandler
from handlers import show_schedule
from config import TELEGRAM_BOT_TOKEN
from dotenv import load_dotenv

load_dotenv()


async def start(update: Update, context):
    await update.message.reply_text("Tap the button to see the schedule")


def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('schedule', show_schedule))

    application.run_polling()


if __name__ == "__main__":
    main()
