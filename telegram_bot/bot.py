import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import setup_dialogs
from aiohttp import web

from routers.ref_code_no_roles.ref_code_no_roles_router import ref_code_no_roles_router
from routers.start_command.start_command_router import start_command_router

from dotenv import load_dotenv, find_dotenv

from telegram_bot.routers.ref_program.balance_dialog.balance_dialog_router import balance_dialog_router
from telegram_bot.routers.ref_program.ref_program_router import ref_program_router

load_dotenv(find_dotenv())

token = os.getenv('token')

BASE_DIR = os.curdir


async def bot_start():
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    #     filename=f'{BASE_DIR}/tg_logs/aiogram.log'
    # )

    bot = Bot(token='7290803644:AAFd3v0SEeSdUxz7HzCOqcgXOMjxmfGt9RQ')

    # redis_connect = os.getenv('REDIS_CONNECT_URL')
    # storage = RedisStorage.from_url(redis_connect, key_builder=DefaultKeyBuilder(with_destiny=True))

    # storage = RedisStorage.from_url('redis://localhost:6379/0', key_builder=DefaultKeyBuilder(with_destiny=True))

    # dp = Dispatcher(storage=storage)

    dp = Dispatcher()

    setup_dialogs(dp)

    dp.include_router(balance_dialog_router)
    dp.include_router(start_command_router)
    dp.include_router(ref_code_no_roles_router)
    dp.include_router(ref_program_router)

    @dp.message(F.document)
    async def get_file_id(message: Message, state: FSMContext):
        await message.answer(
            text=str(message.document.file_id)
        )

    @dp.message(F.photo)
    async def get_file_id(message: Message, state: FSMContext):
        await message.answer(
            text=str(message.photo[0].file_id)
        )

    @dp.message(F.audio)
    async def get_file_id(message: Message, state: FSMContext):
        await message.answer(
            text=str(message.audio.file_id)
        )

    @dp.message(F.text == 'ping')
    async def test_handler_on_ping(message: Message, state: FSMContext):
        await message.answer(
            text='PONG'
        )

    await bot.delete_webhook(
        drop_pending_updates=True
    )
    await dp.start_polling(bot)


async def webserver_start():
    app = web.Application()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 5555)
    await site.start()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task_1 = loop.create_task(bot_start())
    task_2 = loop.create_task(webserver_start())
    loop.run_until_complete(asyncio.gather(task_1, task_2))
