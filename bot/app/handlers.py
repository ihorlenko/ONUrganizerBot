from xml.etree.ElementTree import tostring

from aiogram import Router,F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.enums import ParseMode
import bot.app.keyboards as kb
import bot.app.resources as rs
#import re
router = Router()



@router.message(CommandStart())
async def welcome_msg(message: Message):
    await message.answer("Greetings!", reply_markup = kb.main)

@router.message(F.text.upper() == 'TEST')
async def help(message: Message):
    await message.reply('TEST Placeholder', reply_markup=kb.main)

'''
#God be my witness, I tried to make it work
@router.message(F.text.re.compile(r'\bBYE\b', re.IGNORECASE).match('BYE'))
async def bye_command(message: Message):
    await message.reply('See ya!')
'''

@router.message(F.text.upper() == 'HELP')
async def help_command(message: Message):
    await message.reply('Help Placeholder', reply_markup=kb.inline)


@router.message(F.text.upper() == 'SCHEDULE' )
async def schedule_command(message: Message):
    await message.answer_photo(rs.days_id["the week"],
                        reply_markup = await kb.inline_days())

#tis a utility handler, not to be included with the full release
@router.message(F.photo)
async def photo_id(message: Message):
    await message.answer(f'ID: {message.photo[-1].file_id}')

@router.callback_query(F.data.in_(['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'the week'] ))
async def monday(callback: CallbackQuery):
    day = callback.data
    media = InputMediaPhoto(media=rs.days_id[day])
    await callback.answer(f'Displaying the schedule for {day.lower()}',show_alert=False)
    await callback.message.edit_media(
        media=media,
        caption = f"Schedule for {day.capitalize()}",
        reply_markup = await kb.inline_days()
    )
'''
#for whatever reason this handler was replying to things that other ones should've caught
@router.message()
async def default_handler(message: Message):
    await message.reply("I didn't understand that\\. Please use the command or type *'Help'* for assistance\\."
                    , parse_mode=ParseMode.MARKDOWN_V2)
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