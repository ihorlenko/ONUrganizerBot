from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton as KB,
)


main = ReplyKeyboardMarkup(
    keyboard=[
        [KB(text="Monday"), KB(text="Tuesday"), KB(text="Wednesday")],
        [KB(text="Thursday"), KB(text="Friday"), KB(text="Saturday")],
        [KB(text="Today")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose option",
)
