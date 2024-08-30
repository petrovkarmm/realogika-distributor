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
    print(customer_code)

    data = {
        "Data": {
            "customerCode": customer_code,
            "amount": f"{int(float(shop_item_data.get('amount', 0)))}.00",
            "purpose": (
                           'test\n\n'
                           'test'
                       )[:140],
            "paymentMode": [
                "sbp",
                "card"
            ],
        }
    }
    return data


async def get_payment_link(payment_data: dict):
    jwt = os.getenv('JWT')
    print(jwt)
    url = 'https://enter.tochka.com/uapi/acquiring/v1.0/payments'

    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json"
    }
    print(headers)
    json_formatted_payment_data = json.dumps(payment_data)
    print(json_formatted_payment_data)

    payment_response = requests.post(url=url, headers=headers, data=json.dumps(payment_data))

    if payment_response.status_code == 200:
        print(payment_response.json())
    else:
        print(payment_response.status_code, payment_response.text)
