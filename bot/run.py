import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher
from app.routers import setup_router


load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(TELEGRAM_TOKEN)

dp = Dispatcher()


async def main():
    router = setup_router()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("End")
