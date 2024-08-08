import aiohttp

from telegram_bot.settings import api_url


async def get_all_user_rewards(user_account_id: int):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/rewards?account_id={user_account_id}'
        async with session.get(url) as response:
            return await response.json()


async def get_user_reward(reward_id: int):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/reward/{reward_id}'
        async with session.get(url) as response:
            return await response.json()
