import aiohttp

from telegram_bot.settings import api_url


async def get_my_sponsor_data(user_account_id: int):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/partners/my/sponsors?user_id={user_account_id}'
        async with session.get(url) as response:
            return await response.json()


async def get_my_sponsored_users_data(user_account_id: int):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/partners/my/sponsored?user_id={user_account_id}'
        async with session.get(url) as response:
            return await response.json()


async def get_user_data(user_id: int):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/users/{user_id}'
        async with session.get(url) as response:
            return await response.json()


async def get_user_promocode(user_id: int):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/promocode/simple/{user_id}'
        async with session.get(url) as response:
            return await response.json()
