import os
from dotenv import load_dotenv
import logging
import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from config import close_session, create_session, session

# region Setup
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher()

global session

# endregion


# region Main program
async def main():
    await create_session()

    async def on_shutdown(dispatcher):
        await close_session(session)

    dp.include_router(router)
    await dp.start_polling(bot, on_shutdown=on_shutdown)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("End")
# endregion
