from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Schedule"), KeyboardButton(text="ScheduleV2")]],
    resize_keyboard=True,
    input_field_placeholder="Choose option",
)

inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Google", url="https://google.com")],
        [InlineKeyboardButton(text="Youtube", url="https://youtube.com")],
    ]
)

np_weekdays = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Previous", callback_data="prev"),
            InlineKeyboardButton(text="Next", callback_data="next"),
        ]
    ]
)
