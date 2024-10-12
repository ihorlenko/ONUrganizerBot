from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton as KB,
    InlineKeyboardButton as IKB,
)


from aiogram.types import ReplyKeyboardMarkup as RKM, KeyboardButton as KB

main = RKM(
    keyboard=[
        [KB(text="Понеділок"), KB(text="Вівторок"), KB(text="Середа")],
        [KB(text="Четвер"), KB(text="П’ятниця"), KB(text="Субота")],
        [KB(text="Сьогодні")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Виберіть день тижня",
)



group = InlineKeyboardMarkup(
    inline_keyboard=[
        [IKB(text = "1", callback_data="first"),IKB(text="2", callback_data="second")],
        [IKB(text="3", callback_data="three"), IKB(text="4", callback_data="fourth")]
    ]
)