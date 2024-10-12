from loguru import logger

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram import types
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode

import app.keyboards as kb
from config import bot
from models.models import WeeklySchedule
from app.utils.helpers import load_schedule_from_yaml
from app.utils.helpers import format_schedule_for_day
from app.utils.helpers import translate
import resources.translations as tr


schedule_path = "./bot/resources/schedule.yaml"
schedule_router: Router = Router()
weekly_schedule: WeeklySchedule = load_schedule_from_yaml(schedule_path)

last_day = ""
last_messages = {}



@schedule_router.message(CommandStart())
async def welcome_msg(message: Message):
    logger.info(f"Received /start command from user: {message.from_user.id}")
    
    if message.from_user.id in last_messages:
        try:
            await bot.delete_message(message.chat.id, last_messages[message.from_user.id])
        except Exception as e:
            logger.error(f"Error deleting previous message: {e}")
    await message.answer(
        f"Привіт!👋 Я - бот 122 спеціальності\nНа який день показати розклад?", reply_markup=kb.main
    )


@schedule_router.message(lambda message: message.text.lower() in [
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
    'понеділок', 'вівторок', 'середа', 'четвер', 'п’ятниця'
])
async def send_or_edit_schedule(message: types.Message):
    global last_day
    day_of_week = translate(message.text, tr.day_translation)
    logger.info(f"User {message.from_user.id} requested schedule for: {day_of_week}")


    if day_of_week == last_day:
        logger.info(f"Same day requested ({last_day}), deleting message.")
        await bot.delete_message(message.chat.id, message.message_id)
        return
    last_day = day_of_week
    await bot.delete_message(message.chat.id, message.message_id)
    day_of_week = day_of_week.capitalize()
    daily_schedule = next((schedule for schedule in weekly_schedule.daily_schedules if schedule.day == day_of_week), None)

    if daily_schedule:
        schedule_text = format_schedule_for_day(daily_schedule)


        if message.from_user.id in last_messages:
            try:
                await bot.edit_message_text(
                    text=schedule_text,
                    chat_id=message.chat.id,
                    message_id=last_messages[message.from_user.id],
                    parse_mode=ParseMode.MARKDOWN_V2,
                    disable_web_page_preview=True,
                    reply_markup=kb.group
                )
                logger.info(f"Edited schedule message for user: {message.from_user.id}")
            except Exception as e:
                logger.error(f"Error editing message: {e}")
                msg = await message.answer(
                    schedule_text,
                    parse_mode=ParseMode.MARKDOWN_V2,
                    disable_web_page_preview=True,
                    reply_markup=kb.group
                )
                last_messages[message.from_user.id] = msg.message_id
        else:
            msg = await message.answer(
                schedule_text,
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True,
                reply_markup=kb.group
            )
            last_messages[message.from_user.id] = msg.message_id
    else:
        logger.warning(f"Schedule for {day_of_week} not found for user: {message.from_user.id}")
        await message.answer(f"Розклад на {day_of_week} не знайдено\.", parse_mode=ParseMode.MARKDOWN_V2)