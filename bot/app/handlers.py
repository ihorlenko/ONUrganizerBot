from os import getenv
import random
import json

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import types

from dotenv import load_dotenv
from datetime import datetime

from bot.config import fetch_image_url
from .builders import build_inline_days_kb
import bot.app.keyboards as kb
from .utils.helpers import str_today, num_to_weekday, normalize_day_offset

router = Router()
global session

load_dotenv()
API_KEY = getenv("GOOGLE_TOKEN")
CX = getenv("SE_ID")

with open('bot/resources/search_prompts.json', 'r') as f1, \
        open('bot/resources/days_id.json', 'r') as f2:
    SEARCH_PROMPTS = json.load(f1)
    days_map = json.load(f2)


@router.message(CommandStart())
async def welcome_msg(message: Message):
    await message.answer(
        f"Hello, choose one of the options below", reply_markup=kb.main
    )


@router.message(F.text.lower() == "schedule")
async def schedule_command(message: Message):
    await message.answer_photo(
        days_map["the week"], reply_markup=await build_inline_days_kb()
    )


@router.message(F.text.lower() == "schedulev2")
async def schedule_command(message: Message):
    day_of_week = str_today()
    with open('bot/resources/days_id.json', 'r') as f:
        day_id = json.load(f).get(day_of_week.lower())

    await message.answer_photo(day_id, reply_markup=kb.np_weekdays)


@router.message(F.text.lower() == "bye")
async def bye_command(message: Message):
    await message.reply_sticker(
        "CAACAgIAAxkBAAEFgZZjAAGIEnFk7nzv_wGBIfFyGHdS_XsAAhYAAwC5MAEl49O0W54M1R8E"
    )
    await message.reply("Fare thee well, foreordained straggler")


@router.callback_query(
    F.data.in_(days_map.keys())
)  # the keys are all weekdays + 'the week'
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


@router.callback_query(F.data == "next")
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


@router.callback_query(F.data == "prev")
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


def is_cat_keyword(message: types.Message, keywords: list) -> bool:
    return any(keyword in message.text.upper() for keyword in keywords)


cat_keys = ["CAT", "KITTEN", "KITTY", "CATS", "KITTENS"]


@router.message(lambda message: is_cat_keyword(message, cat_keys))
async def kitten_send(message: types.Message):
    prompt = random.choice(SEARCH_PROMPTS)
    image_url = await fetch_image_url(session, prompt, API_KEY, CX)
    if image_url.startswith("http"):
        try:
            async with session.get(image_url) as response:
                if response.status == 200:
                    await message.reply_photo(image_url)
                else:
                    await message.reply("Image URL is not accessible")
        except Exception as e:
            await message.reply(f"Error fetching image: {e}")
    else:
        await message.reply(image_url)


@router.message(F.photo)
async def photo_id(message: Message):
    await message.reply(f"ID: {message.photo[-1].file_id}")


@router.message(F.video)
async def photo_id(message: Message):
    await message.reply(f"ID: {message.video.file_id}")


"""
#for whatever reason this handler was replying to things that other ones should've caught
@router.message()
async def default_handler(message: Message):
    await message.reply("I didn't understand that\\. Please use the command or type *'Help'* for assistance\\."
                    , parse_mode=ParseMode.MARKDOWN_V2)
"""

"""
#God be my witness, I tried to make it work
@router.message(F.text.re.compile(r'\bBYE\b', re.IGNORECASE).match('BYE'))
async def bye_command(message: Message):
    await message.reply('See ya!')
"""


"""
↓↓↓ MarkdownV2 syntax apparently
*bold \*text*
_italic \*text_
__underline__
~strikethrough~
*bold _italic bold ~italic bold strikethrough~ __underline italic bold___ bold*
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=123456789)
"""
