from dataclasses import dataclass
from datetime import datetime

REWARD_KEY = "reward"


@dataclass
class RewardMovement:
    id: int
    amount: str

    @staticmethod
    def format_amount(amount: int or float):
        return f'Вознаграждение +{amount}'
