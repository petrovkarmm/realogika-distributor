import asyncio

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from scheduler_fetchers import get_all_no_roles_users_ids


async def send_notification_for_no_roles_users(message: Message, state: FSMContext):
    bot_instance = message.bot
    bot_instance: Bot

    no_roles_users_ids = await get_all_no_roles_users_ids()
    for no_role_user_id in no_roles_users_ids:
        await bot_instance.send_message(
            text='Шедулер 1.',
            chat_id=no_role_user_id
        )
        await asyncio.sleep(3,5)
