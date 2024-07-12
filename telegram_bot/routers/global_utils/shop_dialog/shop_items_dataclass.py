from dataclasses import dataclass
from datetime import datetime

SHOP_KEY = "shop"


@dataclass
class ShopItem:
    id: int
    title: str

    @staticmethod
    def counter_checker(count: int, title: str):
        if count <= 0:
            return f"{title} | Отсутствует"
        return title
