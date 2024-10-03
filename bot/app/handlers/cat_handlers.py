import random

from aiogram import Router
from aiogram import types

from config import fetch_image_url
from utils.helpers import is_cat_keyword

cat_router = Router()


# TODO: for better times
# @cat_router.message(lambda message: is_cat_keyword(message, cat_keys))
# async def kitten_send(message: types.Message):
#     SEARCH_PROMPTS = ['cat']
#     prompt = random.choice(SEARCH_PROMPTS)
#     image_url = await fetch_image_url(session, prompt, API_KEY, CX)
#     if image_url.startswith("http"):
#         try:
#             async with session.get(image_url) as response:
#                 if response.status == 200:
#                     await message.reply_photo(image_url)
#                 else:
#                     await message.reply("Image URL is not accessible")
#         except Exception as e:
#             await message.reply(f"Error fetching image: {e}")
#     else:
#         await message.reply(image_url)