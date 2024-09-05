from telegram import Update
from telegram.ext import ContextTypes
from config import SCHEDULE_IMAGE_PATH


async def show_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    with open(SCHEDULE_IMAGE_PATH, 'rb') as image:
        await context.bot.send_photo(chat_id=chat_id, photo=image)
