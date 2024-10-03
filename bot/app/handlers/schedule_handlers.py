from os import getenv
import json

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from dotenv import load_dotenv
from datetime import datetime

from app.builders import build_inline_days_kb
import app.keyboards as kb
from app.utils.helpers import str_today, num_to_weekday, normalize_day_offset

schedule_router = Router()

load_dotenv()

with open('bot/resources/days_id.json', 'r') as f:
    days_map = json.load(f)


@schedule_router.message(CommandStart())
async def welcome_msg(message: Message):
    await message.answer(
        f"Hello, choose one of the options below", reply_markup=kb.main
    )


@schedule_router.message(F.text.lower() == "schedule")
async def schedule_command(message: Message):
    await message.answer_photo(
        days_map["the week"], reply_markup=await build_inline_days_kb()
    )


@schedule_router.message(F.text.lower() == "schedulev2")
async def schedule_command(message: Message):
    day_of_week = str_today()
    with open('bot/resources/days_id.json', 'r') as f:
        day_id = json.load(f).get(day_of_week.lower())

    await message.answer_photo(day_id, reply_markup=kb.np_weekdays)


@schedule_router.message(F.text.lower() == "bye")
async def bye_command(message: Message):
    await message.reply_sticker(
        "CAACAgIAAxkBAAEFgZZjAAGIEnFk7nzv_wGBIfFyGHdS_XsAAhYAAwC5MAEl49O0W54M1R8E"
    )
    await message.reply("Fare thee well, foreordained straggler")


@schedule_router.callback_query(
    F.data.in_(days_map.keys())
)
async def schedule_reply(callback: CallbackQuery):
    day = callback.data
    media = InputMediaPhoto(media=days_map[day])
    await callback.answer(
        f"Displaying the schedule for {day.lower()}", show_alert=False
    )
    await callback.message.edit_media(
        media=media,
        caption=f"Schedule for {day.capitalize()}",
        reply_markup=await build_inline_days_kb(),
    )


@schedule_router.callback_query(F.data == "next")
async def next_day(callback: CallbackQuery):

    global day_offset
    day_offset = normalize_day_offset(day_offset + 1)
    current_weekday = datetime.today().weekday()
    day_of_week = num_to_weekday((current_weekday + day_offset) % 7)
    media = InputMediaPhoto(media=days_map[day_of_week])

    await callback.answer(
        f"Displaying the schedule for {day_of_week.lower()}", show_alert=False
    )
    await callback.message.edit_media(
        media=media,
        caption=f"Schedule for {day_of_week.capitalize()}",
        reply_markup=kb.np_weekdays,
    )


@schedule_router.callback_query(F.data == "prev")
async def next_day(callback: CallbackQuery):

    global day_offset
    day_offset = normalize_day_offset(day_offset - 1)
    current_weekday = datetime.today().weekday()
    day_of_week = num_to_weekday((current_weekday + day_offset) % 7)
    media = InputMediaPhoto(media=days_map[day_of_week])

    await callback.answer(
        f"Displaying the schedule for {day_of_week.lower()}", show_alert=False
    )
    await callback.message.edit_media(
        media=media,
        caption=f"Schedule for {day_of_week.capitalize()}",
        reply_markup=kb.np_weekdays,
    )


@schedule_router.message(F.photo)
async def photo_id(message: Message):
    await message.reply(f"ID: {message.photo[-1].file_id}")


