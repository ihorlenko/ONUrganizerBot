import os
from dotenv import load_dotenv
import logging
import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router

#region Setup
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher()
#endregion


#region Main program
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('End')
#endregion
