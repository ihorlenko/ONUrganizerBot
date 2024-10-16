import asyncio
from loguru import logger

from app.routers import setup_router
from config import dp, bot


async def main():
    router = setup_router()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.remove()
        logger.add("bot.log", rotation="1 MB", level="INFO")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("End")
