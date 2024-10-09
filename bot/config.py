import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher


load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(TELEGRAM_TOKEN)

dp = Dispatcher()