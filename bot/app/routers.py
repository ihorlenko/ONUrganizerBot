from aiogram import Router
from app.handlers.schedule_handlers import schedule_router

def setup_router():
    router = Router()

    # Include as many other routers as needed here
    router.include_routers(schedule_router)

    return router