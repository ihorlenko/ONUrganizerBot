from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup, KeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Send photo')]
], resize_keyboard=True, input_field_placeholder="Choose option")

inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Google', url='https://google.com')],
    [InlineKeyboardButton(text='Youtube', url='https://youtube.com')]
])
