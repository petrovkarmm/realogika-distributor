from dataclasses import dataclass
from datetime import datetime

BALANCE_KEY = "balance"


@dataclass
class BalanceMovement:
    id: int
    amount: str

    @staticmethod
    def format_amount(amount: int or float, is_accrual: bool):
        """
        Отображения плюса и минуса в зависимости от типа передвижения
        """
        if is_accrual:
            return f'Пополнение {amount}'
        return f'Списание {amount}'
