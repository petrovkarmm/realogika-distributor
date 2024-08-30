import json
import os

import requests
import validators
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
token = os.getenv("token")


def validate_image_url(item_url_image: str) -> str:
    fallback_image = 'https://th.bing.com/th/id/OIP.Nskk7OgDwsE73BbF1kYVLwAAAA?rs=1&pid=ImgDetMain'
    if not validators.url(item_url_image):
        return fallback_image

    try:
        response = requests.get(item_url_image, timeout=5)
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            return item_url_image
        else:
            return fallback_image
    except requests.RequestException:
        return fallback_image


async def form_invoice_data(shop_item_data: dict):
    customer_code = os.getenv('CUSTOMER_CODE')

    data = {
        "Data": {
            "customerCode": customer_code,
            "amount": f"{int(float(shop_item_data.get('amount', 0)))}.00",
            "purpose": (
                           f'{shop_item_data.get("name")}'
                       )[:140],
            "paymentMode": [
                "sbp",
                "card"
            ],
        }
    }
    return data
