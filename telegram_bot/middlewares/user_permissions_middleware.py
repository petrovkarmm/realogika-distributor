import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from routers.start_command.start_command_fetchers import get_user_partner_start


class UserPermissions(BaseMiddleware):
    def __init__(self, sleep_sec: int):
        self.sleep_sec = sleep_sec

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user_permission_data = await get_user_partner_start(event.message.from_user.id)
        if user_permission_data:
            result = await handler(event, data)
            return result
        else:
            await event.message.answer(
                'test'
            )

