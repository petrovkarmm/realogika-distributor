import aiohttp

from settings import api_url, headers


async def get_all_no_roles_users_ids():
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/partners/my/sponsors?'
        async with session.get(url=url, headers=headers) as response:
            return await response.json()

