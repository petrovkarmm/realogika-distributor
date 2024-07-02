import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import TelegramObject
from aiogram_dialog import DialogManager


class UserStatusCheckMessage(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        # Запрос на получение инстанса юзерa
        result = await handler(event, data)
        return result


class UserStatusCheckCallback(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        # Запрос на получение инстанса юзера
        result = await handler(event, data)
        return result
