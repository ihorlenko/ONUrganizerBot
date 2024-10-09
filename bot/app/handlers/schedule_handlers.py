import random

from dotenv import load_dotenv
from loguru import logger

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import asyncio
from app.utils.helpers import load_schedule_from_yaml
from config import bot

from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from models.models import WeeklySchedule
from models.models import DailySchedule
from aiogram.utils.text_decorations import markdown_decoration

from app.keyboards import group

last_day = ""

schedule_path = "./bot/resources/schedule.yaml"
schedule_router: Router = Router()
weekly_schedule: WeeklySchedule = load_schedule_from_yaml(schedule_path)

load_dotenv()

logger.add("bot.log", rotation="1 MB", level="INFO")


def escape_md(*content, sep=" "):
    def _join(*content, sep=" "):
        return sep.join(map(str, content))

    return markdown_decoration.quote(_join(*content, sep=sep))


bells = [
    "08:00",
    "09:30",
    "11:20",
    "12:50",
    "14:20",
    "15:50",
]

last_messages = {}


def format_schedule_for_day(daily_schedule: DailySchedule) -> str:
    logger.info(f"Formatting schedule for day: {daily_schedule.day}")
    result = []
    result.append(f"*{escape_md(daily_schedule.day.upper())}:*\n")
    classes = daily_schedule.classes

    for university_class in sorted(classes, key=lambda c: c.class_time.start_time):
        subject = escape_md(university_class.subject.name)
        teacher = escape_md(university_class.subject.teacher.name)
        class_type = escape_md(university_class.class_type.class_type)
        start_time = escape_md(university_class.class_time.start_time.strftime('%H:%M'))
        end_time = escape_md(university_class.class_time.end_time.strftime('%H:%M'))
        classroom = university_class.classroom.room_number

        class_order = bells.index(start_time) + 1

        classroom = f"{escape_md(classroom)} аудиторії" if classroom != "online" else "online"
        class_type = "Лекція" if class_type == "lecture" else "Практика"
        class_type += " в" if classroom != "online" else ""

        teacher_name = escape_md(university_class.subject.teacher.name)
        if university_class.subject.teacher.link:
            teacher = f"[{teacher_name}]({university_class.subject.teacher.link})"
        else:
            teacher = teacher_name

        subgroups_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
        subgroups = list(map(lambda s: subgroups_emojis[s.number - 1], university_class.subgroups))
        subgroups = ', '.join(subgroups)
        subgroups = escape_md(subgroups)

        result.append(
            f"*{class_order} пара:* {start_time}\-{end_time}\n"
            f"*{subject}* \- {teacher}\n"
            f"{class_type} {classroom}\n"
            f"*Підгрупи:* {subgroups}")

        result.append("")

    return "\n".join(result)


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


# utility handler
@schedule_router.message(F.photo)
async def photo_id(message: Message):
    logger.info(f"Received photo from user: {message.from_user.id}")
    await message.reply(f'ID: {message.photo[-1].file_id}')


@schedule_router.message(lambda message: message.text.lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'])
async def send_or_edit_schedule(message: types.Message, state: FSMContext):
    global last_day
    logger.info(f"User {message.from_user.id} requested schedule for: {message.text}")
    if message.text.lower() == last_day:
        logger.info(f"Same day requested ({last_day}), deleting message.")
        await bot.delete_message(message.chat.id, message.message_id)
        return
    last_day = message.text.lower()
    await bot.delete_message(message.chat.id, message.message_id)
    day_of_week = message.text.capitalize()
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
                    reply_markup=group
                )
                logger.info(f"Edited schedule message for user: {message.from_user.id}")
            except Exception as e:
                logger.error(f"Error editing message: {e}")
                msg = await message.answer(
                    schedule_text,
                    parse_mode=ParseMode.MARKDOWN_V2,
                    disable_web_page_preview=True,
                    reply_markup=group
                )
                last_messages[message.from_user.id] = msg.message_id
        else:
            msg = await message.answer(
                schedule_text,
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True,
                reply_markup=group
            )
            last_messages[message.from_user.id] = msg.message_id
    else:
        logger.warning(f"Schedule for {day_of_week} not found for user: {message.from_user.id}")
        await message.reply(f"Розклад на {day_of_week} не знайдено.", parse_mode=ParseMode.MARKDOWN_V2)