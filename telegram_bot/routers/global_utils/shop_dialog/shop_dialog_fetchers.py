import aiohttp

from settings import api_url, headers


async def get_all_items_from_shop(user_id: int):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/items?user_external_id={user_id}'
        async with session.get(url=url, headers=headers) as response:
            return await response.json()


async def get_item_from_shop(item_id):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/item/{item_id}'
        async with session.get(url=url, headers=headers) as response:
            return await response.json()


async def post_create_payment(payment_data: dict):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/payment'
        async with session.post(url=url, headers=headers, json=payment_data) as response:
            return await response.json()


async def patch_change_payment_status(payment_id: str):
    async with aiohttp.ClientSession() as session:
        url = f'{api_url}/payment/{payment_id}'
        async with session.patch(url=url, headers=headers) as response:
            return await response.json()
