from aiogram import Router,F
from aiogram.filters import CommandStart
from aiogram.types import Message
import bot.app.keyboards as kb
router = Router()


@router.message(CommandStart())
async def welcome_msg(message: Message):
    await message.answer("Greetings!", reply_markup=kb.main)


@router.message(F.text.upper() == 'HELP')
async def help(message: Message):
    await message.reply('Help Placeholder', reply_markup=kb.inline)

