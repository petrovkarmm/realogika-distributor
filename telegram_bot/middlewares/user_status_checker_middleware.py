# import logging
# from typing import Callable, Dict, Any, Awaitable
# from aiogram import BaseMiddleware
# from aiogram.enums import ChatType
# from aiogram.fsm.context import FSMContext
# from aiogram.types import TelegramObject
# from aiogram_dialog import DialogManager
#
# from telegram_bot.routers.global_utils.global_fetchers import get_user_data
#
#
# class UserStatusCheckMessage(BaseMiddleware):
#     async def __call__(
#             self,
#             handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#             event: TelegramObject,
#             data: Dict[str, Any],
#     ) -> Any:
#         state = data["state"]
#         state: FSMContext
#
#         current_user_state = await state.get_state()
#
#         user_id = event.from_user.id
#         user_data = await get_user_data(user_id)
#
#         if user_data['account']['account_partner_roles']:
#             result = await handler(event, data)
#             return result
#         elif user_data['account']['account_partner_roles'] and not current_user_state:
#             await event.answer(
#                 text=''
#             )
#         else:
#             await event.answer(
#                 'У вас отсутствует роль. '
#             )
#         await event.answer(
#
#         )
#
#
