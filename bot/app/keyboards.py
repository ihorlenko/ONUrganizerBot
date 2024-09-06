from aiogram.types import (InlineKeyboardButton,InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,KeyboardButton)

# TODO: Have to meet code style conventions decared in PEP
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'help')],
    [KeyboardButton(text = 'Hello!'),KeyboardButton(text = 'Bye!')]
])

inline = InlineKeyboardMarkup ( inline_keyboard=[
    [InlineKeyboardButton(text='Google',url = 'google.com')],
    [InlineKeyboardButton(text='Youtube', url='youtube.com')]

])

