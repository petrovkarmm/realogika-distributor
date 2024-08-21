import aiohttp

from settings import api_url, headers


async def patch_user_promocode(promocode_name: str, telegram_user_id: int, sponsored_user_data: dict):
    async with aiohttp.ClientSession() as session:
        url = (f'{api_url}/users/partner/link?'
               f'user_external_id={telegram_user_id}&'
               f'promocode={promocode_name}')
        async with session.patch(url=url, headers=headers, json=sponsored_user_data) as response:
            status_code = response.status
            promocode_response = await response.json()
            return status_code, promocode_response


async def get_shop_item_id(offer_id: int):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/offers/{offer_id}'
        async with session.get(url=url, headers=headers) as response:
            return await response.json()


async def get_sponsor_user_data(account_id: int):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/user_accounts/{account_id}'
        async with session.get(url=url, headers=headers) as response:
            return await response.json()


async def get_user_partner_start(telegram_id: int):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/partners/user/start/?external_id={telegram_id}'
        async with session.get(url=url, headers=headers) as response:
            return await response.json()

