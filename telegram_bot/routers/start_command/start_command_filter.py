from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class MainAdminsFilter(BaseFilter):
    def __init__(self):
        self.admins_external_id = [361153663]

    async def __call__(self, message: Message) -> bool:  # [3]
        return message.from_user.id in self.admins_external_id