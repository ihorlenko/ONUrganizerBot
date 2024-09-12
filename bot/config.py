from aiohttp import ClientSession
import random

global session

async def create_session():
    global session
    session = ClientSession()


async def fetch_image_url(session, prompt, api_key, cx):
    url = f'https://www.googleapis.com/customsearch/v1?q={prompt}&key={api_key}&cx={cx}&searchType=image&start={random.randint(1, 10) * 10}'

    async with session.get(url) as response:
        data = await response.json()
        items = data.get('items', [])
        if items:
            image = random.choice(items)
            return image['link']
        else:
            return "No images found"


async def close_session():
    if session:
        await session.close()