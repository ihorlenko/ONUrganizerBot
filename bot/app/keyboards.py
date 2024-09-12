from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Schedule'),KeyboardButton(text='ScheduleV2')]
], resize_keyboard=True, input_field_placeholder="Choose option")

inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Google', url='https://google.com')],
    [InlineKeyboardButton(text='Youtube', url='https://youtube.com')]
])

#region Schedule keyboards
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','The Week']
async def inline_days():
    kb = InlineKeyboardBuilder()
    for day in days:
        kb.add(InlineKeyboardButton(text=day, callback_data=f'{day.lower()}'))
    return kb.adjust(2).as_markup()

np_weekdays = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Previous', callback_data='prev'),
     InlineKeyboardButton(text='Next', callback_data='next')]
])
#endregion