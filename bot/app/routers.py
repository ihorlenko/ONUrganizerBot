from aiogram import Router
from bot.app.handlers.schedule_handlers import schedule_router
from handlers.cat_handlers import cat_router

def setup_router():
    router = Router()

    # Include as many other routers as needed here
    router.include_routers(schedule_router)

    return router