from aiogram import Router,F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode
import bot.app.keyboards as kb
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

@router.message()
async def default_handler(message: Message):
    await message.reply("I didn't understand that\\. Please use the command or type *'Help'* for assistance\\."
                        , parse_mode=ParseMode.MARKDOWN_V2)

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