from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton as KB,
    InlineKeyboardButton as IKB,
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
group = InlineKeyboardMarkup(
    inline_keyboard=[
        [IKB(text = "1", callback_data="first"),IKB(text="2", callback_data="second")],
        [IKB(text="3", callback_data="three"), IKB(text="4", callback_data="fourth")]
    ]
)