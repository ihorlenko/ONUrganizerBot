from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Send photo')]
], resize_keyboard=True, input_field_placeholder="Choose option")

inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Google', url='https://google.com')],
    [InlineKeyboardButton(text='Youtube', url='https://youtube.com')]
])
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','The Week']
async def inline_days():
    kb = InlineKeyboardBuilder()
    for day in days:
        kb.add(InlineKeyboardButton(text=day, callback_data=f'{day.lower()}'))
    return kb.adjust(2).as_markup()