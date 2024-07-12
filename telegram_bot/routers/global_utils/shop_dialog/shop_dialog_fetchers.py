import aiohttp

from telegram_bot.settings import api_url


async def get_all_shop_items():
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/items'
        async with session.get(url) as response:
            return await response.json()
