from dataclasses import dataclass
from datetime import datetime

SHOP_KEY = "shop"


@dataclass
class ShopItem:
    id: int
    name: str
    price: int or float
    description: str

    @staticmethod
    def counter_checker(count: int, name: str):
        if count <= 0:
            return f"{name} | Отсутствует"
        return name
