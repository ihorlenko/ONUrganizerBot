from os import getenv
from aiogram import Router,F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.enums import ParseMode
from dotenv import load_dotenv

import bot.app.keyboards as kb
import bot.app.resources as rs
from datetime import datetime
from bot.app.resources import to_key
from aiohttp import ClientSession
from aiogram import types
#import re
import requests
import random

#region Variables
router = Router()
day_offset = 0 # offset for schedulev2
#endregion

#region Google API setup
load_dotenv()
API_KEY = getenv('GOOGLE_TOKEN')
CX = getenv('SE_ID')
SEARCH_PROMPTS = ['funny kitten photo', 'kitten sunbathing photo', 'kittens photo', 'kitten jumping photo']
#endreggion

def normalize_offset(offset):
    return (offset % 7 + 7) % 7

#region Mundane handlers
@router.message(CommandStart())
async def welcome_msg(message: Message):
    user_name = message.from_user.first_name
    current_time = datetime.now().strftime('%H:%M')
    await message.answer(f"Hello, {user_name}! It's {current_time} — welcome!", reply_markup=kb.main)

@router.message(F.text.upper() == 'TEST')
async def help(message: Message):
    await message.reply('TEST Placeholder', reply_markup=kb.main)

@router.message(F.text.upper() == 'HELP')
async def help_command(message: Message):
    await message.reply('Help Placeholder', reply_markup=kb.inline)

@router.message(F.text.upper() == 'BYE')
async def bye_command(message: Message):
    await message.reply_sticker("CAACAgIAAxkBAAEFgZZjAAGIEnFk7nzv_wGBIfFyGHdS_XsAAhYAAwC5MAEl49O0W54M1R8E")
    await message.reply("Fare thee well, foreordained straggler")
#endregion


#region ScheduleV1
@router.message(F.text.upper() == 'SCHEDULE' )
async def schedule_command(message: Message):
    await message.answer_photo(rs.days_id["the week"],
                        reply_markup = await kb.inline_days())

@router.callback_query(F.data.in_(rs.days_id.keys())) # the keys are all weekdays + 'the week'
async def schedule_reply(callback: CallbackQuery):
    day = callback.data
    media = InputMediaPhoto(media=rs.days_id[day])
    await callback.answer(f'Displaying the schedule for {day.lower()}',show_alert=False)
    await callback.message.edit_media(
        media=media,
        caption = f"Schedule for {day.capitalize()}",
        reply_markup = await kb.inline_days()
    )
#endregion


#region ScheduleV2
@router.message(F.text.upper() == 'SCHEDULEV2')
async def schedule_command(message: Message):
    day_of_week = rs.to_key[datetime.today().weekday()]
    await message.answer_photo(rs.days_id[day_of_week],
                        reply_markup = kb.np_weekdays)


@router.callback_query(F.data == 'next')
async def next_day( callback: CallbackQuery):

    global day_offset
    day_offset = normalize_offset(day_offset + 1)
    current_weekday = datetime.today().weekday()
    day_of_week = to_key[(current_weekday + day_offset) % 7]
    media = InputMediaPhoto(media=rs.days_id[day_of_week])

    await callback.answer(f'Displaying the schedule for {day_of_week.lower()}', show_alert=False)
    await callback.message.edit_media(
        media=media,
        caption = f"Schedule for {day_of_week.capitalize()}",
        reply_markup=kb.np_weekdays
    )

@router.callback_query(F.data == 'prev')
async def next_day(callback: CallbackQuery):

    global day_offset
    day_offset = normalize_offset(day_offset - 1)
    current_weekday = datetime.today().weekday()
    day_of_week = to_key[(current_weekday + day_offset) % 7]
    media = InputMediaPhoto(media=rs.days_id[day_of_week])

    await callback.answer(f'Displaying the schedule for {day_of_week.lower()}', show_alert=False)
    await callback.message.edit_media(
        media=media,
        caption=f"Schedule for {day_of_week.capitalize()}",
        reply_markup=kb.np_weekdays
    )
#endregion


#region Unnecessary
async def get_random_kitten_image():
    prompt = random.choice(SEARCH_PROMPTS)
    url = f'https://www.googleapis.com/customsearch/v1?q={prompt}&key={API_KEY}&cx={CX}&searchType=image'

    async with ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            items = data.get('items', [])
            if items:
                image = random.choice(items)
                return image['link']
            else:
                return "No images found"

def is_cat_keyword(message: types.Message, keywords: list) -> bool:
    return any(keyword in message.text.upper() for keyword in keywords)

cat_keys = ['CAT','KITTEN','KITTY','CATS','KITTENS']
@router.message(lambda message: is_cat_keyword(message, cat_keys))
async def kitten_send(message: Message):
    image_url = await get_random_kitten_image()
    if image_url.startswith("http"):
        try:
            async with ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        await message.reply_photo(image_url)
                    else:
                        await message.reply("Image URL is not accessible")
        except Exception as e:
            await message.reply(f"Error fetching image: {e}")
    else:
        await message.reply(image_url)


#endregion


#region utilities
@router.message(F.photo)
async def photo_id(message: Message):
    await message.reply(f'ID: {message.photo[-1].file_id}')

@router.message(F.video)
async def photo_id(message: Message):
    await message.reply(f'ID: {message.video.file_id}')
#endregion


#region Unfinished and Useless
'''
#for whatever reason this handler was replying to things that other ones should've caught
@router.message()
async def default_handler(message: Message):
    await message.reply("I didn't understand that\\. Please use the command or type *'Help'* for assistance\\."
                    , parse_mode=ParseMode.MARKDOWN_V2)
'''

'''
#God be my witness, I tried to make it work
@router.message(F.text.re.compile(r'\bBYE\b', re.IGNORECASE).match('BYE'))
async def bye_command(message: Message):
    await message.reply('See ya!')
'''


'''
↓↓↓ MarkdownV2 syntax apparently
*bold \*text*
_italic \*text_
__underline__
~strikethrough~
*bold _italic bold ~italic bold strikethrough~ __underline italic bold___ bold*
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=123456789)
'''
#endregion