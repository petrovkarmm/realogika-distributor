import aiohttp

from telegram_bot.settings import api_url


async def get_my_sponsor_data(user_id: int):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/partners/my/sponsors?user_id=30'
        async with session.get(url) as response:
            return await response.json()


async def get_my_sponsored_users_data(user_id: int):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/partners/my/sponsored?user_id=30'
        async with session.get(url) as response:
            return await response.json()