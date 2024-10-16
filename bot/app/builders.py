from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.utils.helpers import num_to_weekday


async def build_inline_days_kb():
    kb = InlineKeyboardBuilder()
    weekdays = [num_to_weekday(day) for day in range(2, 8)]

    for day in weekdays:
        kb.add(InlineKeyboardButton(text=day, callback_data=day))
    kb.add(InlineKeyboardButton(text="The Week", callback_data='the week'))
    return kb.adjust(2).as_markup()