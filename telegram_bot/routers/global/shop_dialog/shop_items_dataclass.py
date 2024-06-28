from dataclasses import dataclass
from datetime import datetime

SHOP_KEY = "shop"


@dataclass
class ShopItem:
    id: int
    name: str
    count: int
    price: int or float
    description: str
