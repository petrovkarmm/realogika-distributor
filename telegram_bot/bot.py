import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, PreCheckoutQuery
from aiogram_dialog import setup_dialogs, DialogManager
from routers.ref_code_no_roles.ref_code_no_roles_router import ref_code_no_roles_router
from routers.start_command.start_command_router import start_command_router

from dotenv import load_dotenv, find_dotenv

from routers.global_utils.shop_dialog.shop_dialog_fetchers import patch_change_payment_status
from routers.global_utils.shop_dialog.shop_dialog_router import shop_dialog_router
from routers.global_utils.shop_dialog.shop_dialog_states import ShopDialog
from routers.global_utils.global_handler import global_handlers_router
from routers.global_utils.balance_dialog.balance_dialog_router import balance_dialog_router
from routers.start_command.keyboards import main_menu_keyboard
from settings import BOT_BASE_DIR

load_dotenv(find_dotenv())

token = os.getenv('token')

BASE_DIR = os.curdir

DEBUG = True


async def task(message: Message, state: FSMContext):
    await message.answer(
        text='Привет 1'
    )
    await asyncio.sleep(20)
    await message.answer(
        text='Привет 2'
    )


async def bot_start():
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    #     filename=f'{BOT_BASE_DIR}/tg_logs/aiogram.log'
    # )

    if not DEBUG:
        bot_token = os.getenv('token')
        redis_connect = os.getenv('REDIS_CONNECT_URL')
    else:
        bot_token = '6663031505:AAHf_DCwgkjRZLvGPtX_cwppY3E0qDdKEQw'
        # redis_connect = os.getenv('REDIS_TEST_CONNECT_URL')

    bot = Bot(token=bot_token)
    # storage = RedisStorage.from_url(redis_connect, key_builder=DefaultKeyBuilder(with_destiny=True))

    # dp = Dispatcher(storage=storage)
    dp = Dispatcher()
    setup_dialogs(dp)

    dp.include_router(balance_dialog_router)
    dp.include_router(shop_dialog_router)

    dp.include_router(global_handlers_router)
    dp.include_router(start_command_router)
    dp.include_router(ref_code_no_roles_router)

    @dp.pre_checkout_query(lambda query: True)
    async def checkout_process(pre_checkout_query: PreCheckoutQuery):
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    @dp.message(F.successful_payment)
    async def on_successful_payment(
            message: Message,
            state: FSMContext,
            dialog_manager: DialogManager
    ):
        """
        Запуск диалогового окна магазина с эквайрингом на оплату внутри.
        :param dialog_manager:
        :param message:
        :param state:
        :return:
        """
        # TODO добавить отправку сообщения о покупке верхушке.
        state_data = await state.get_data()
        try:
            invoice_object = state_data['invoice_object']
            invoice_object: Message
        except KeyError:
            current_state = await state.get_state()

            await state.set_state(
                'ref_program_menu'
            )

            await asyncio.sleep(1)

            await message.answer(
                text='Добро пожаловать в магазин.',
                reply_markup=types.ReplyKeyboardRemove()
            )

            await asyncio.sleep(1)

            await dialog_manager.start(
                state=ShopDialog.shop_dialog_menu,
                data=current_state
            )
        else:
            try:
                await invoice_object.delete()
            except Exception as E:
                pass
            else:
                try:
                    text_after_payment = state_data['text_after_payment']
                except KeyError:
                    await state.set_state(
                        'ref_program_menu'
                    )
                    current_payload = state_data['current_payload']
                    await patch_change_payment_status(current_payload)

                    await asyncio.sleep(1)

                    current_state = await state.get_state()

                    await asyncio.sleep(1)

                    await message.answer(
                        text='Добро пожаловать в магазин.',
                        reply_markup=types.ReplyKeyboardRemove()
                    )

                    await asyncio.sleep(1)

                    await dialog_manager.start(
                        state=ShopDialog.shop_dialog_menu,
                        data=current_state
                    )
                else:
                    await state.set_state(
                        'ref_program_menu'
                    )
                    current_payload = state_data['current_payload']
                    payment_status = await patch_change_payment_status(current_payload)

                    await asyncio.sleep(1)

                    await message.answer(
                        text=text_after_payment
                    )

                    current_state = await state.get_state()

                    await asyncio.sleep(1)

                    await message.answer(
                        text='Добро пожаловать в магазин.',
                        reply_markup=types.ReplyKeyboardRemove()
                    )

                    await asyncio.sleep(1)

                    await dialog_manager.start(
                        state=ShopDialog.shop_dialog_menu,
                        data=current_state
                    )

    @dp.message(F.text == 'test_payment')
    async def test_payment(message: Message, state: FSMContext):
        user_id = message.from_user.id
        random_price = 1000

    @dp.message(F.text == 'test_state')
    async def none_state_handler(message: Message, state: FSMContext):
        await state.set_state(
            None
        )

    @dp.callback_query(F.callback.startswith('lesson'))
    async def send_next_video_lesson(message: Message, state: FSMContext):
        # Гет запрос на получение следующего видео видео.
        # Отправка видео.
        # Создание таски с отправкой данные дальше?
        pass

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

    @dp.message(Command('id'))
    async def send_user_id(message: Message, state: FSMContext):
        await message.answer(
            text=str(message.from_user.id)
        )

    await bot.delete_webhook(
        drop_pending_updates=True
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(bot_start())
    except Exception as e:
        print(e)
    else:
        print('bot starting.')
