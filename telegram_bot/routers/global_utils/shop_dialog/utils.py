import requests
import validators


def validate_image_url(item_url_image: str) -> str:
    # URL заглушки
    fallback_image = 'https://th.bing.com/th/id/OIP.Nskk7OgDwsE73BbF1kYVLwAAAA?rs=1&pid=ImgDetMain'

    # Проверка формата URL
    if not validators.url(item_url_image):
        return fallback_image

    try:
        # Запрос к URL
        response = requests.get(item_url_image, timeout=5)
        # Проверка статуса и типа контента
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            return item_url_image
        else:
            return fallback_image
    except requests.RequestException:
        # В случае ошибки запроса возвращаем заглушку
        return fallback_image