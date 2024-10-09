import asyncio
from app.routers import setup_router
from config import dp, bot


async def main():
    router = setup_router()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("End")
