import requests
import validators


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
