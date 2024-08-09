import aiohttp

from telegram_bot.settings import api_url


async def patch_user_promocode(promocode_name: str, telegram_user_id: int):
    async with aiohttp.ClientSession() as session:
        url = (f'{api_url}/users/partner/link?'
               f'user_external_id={telegram_user_id}&'
               f'promocode={promocode_name}')
        async with session.patch(url) as response:
            status_code = response.status
            promocode_response = await response.json()
            return status_code, promocode_response
