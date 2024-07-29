import asyncio

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from telegram_bot.routers.global_utils.balance_dialog.balance_dialog_states import BalanceDialog
from telegram_bot.routers.global_utils.keyboards import ref_program_menu
from telegram_bot.routers.global_utils.shop_dialog.shop_dialog_states import ShopDialog

global_handlers_router = Router()


@global_handlers_router.message(StateFilter('ref_program_menu'), F.text == 'Магазин')
async def global_shop_handler(message: Message, state: FSMContext, dialog_manager: DialogManager):
    """
    Запуск диалогового окна магазина с эквайрингом на оплату внутри.
    :param dialog_manager:
    :param message:
    :param state:
    :return:
    """
    current_state = await state.get_state()

    await message.answer(
        text='Добро пожаловать в магазин.',
        reply_markup=types.ReplyKeyboardRemove()
    )

    await dialog_manager.start(
        state=ShopDialog.shop_dialog_menu,
        data=current_state
    )


@global_handlers_router.message(StateFilter('on_invoice_payment'),
                                F.text == 'Отменить покупку')
async def cancel_payment(message: Message, state: FSMContext, dialog_manager: DialogManager):
    state_data = await state.get_data()
    try:
        invoice_object = state_data['invoice_object']
        invoice_object: Message
    except KeyError:
        current_state = await state.get_state()

        await message.answer(
            text='Добро пожаловать в магазин.',
            reply_markup=types.ReplyKeyboardRemove()
        )

        await dialog_manager.start(
            state=ShopDialog.shop_dialog_menu,
            data=current_state
        )
    else:
        try:
            await invoice_object.delete()
        except Exception as E:
            pass
        current_state = await state.get_state()

        await message.answer(
            text='Добро пожаловать в магазин.',
            reply_markup=types.ReplyKeyboardRemove()
        )

        await dialog_manager.start(
            state=ShopDialog.shop_dialog_menu,
            data=current_state
        )


@global_handlers_router.message(F.text == 'Реф. программа')
async def ref_program_menu_handler(message: Message, state: FSMContext):
    await state.set_state(
        'ref_program_menu'
    )
    await message.answer(
        text='Спонсор - такой-то.\n'
             'Ссылка на телеграм - такая-то(при наличии)\n'
             'Имя такое-то.',
        reply_markup=ref_program_menu()
    )


@global_handlers_router.message(StateFilter('ref_program_menu'), F.text == 'Баланс')
async def open_balance_dialog_handler(message: Message, state: FSMContext, dialog_manager: DialogManager):
    """
    Открытие диалога с балансом
    :param message:
    :param state:
    :param dialog_manager:
    :return:
    """

    await message.answer(
        text='Выберите интересующее пополнение/списание:',
        reply_markup=types.ReplyKeyboardRemove()
    )

    await dialog_manager.start(
        state=BalanceDialog.balance_dialog_menu
    )


@global_handlers_router.message(StateFilter('ref_program_menu'), F.text == 'Моя структура')
async def open_my_arch_handler(message: Message, state: FSMContext):
    pass


@global_handlers_router.message(StateFilter('ref_program_menu'), F.text == 'Моя реф. ссылка')
async def open_my_ref_link(message: Message, state: FSMContext):
    await message.answer(
        text='Ваша ссылка: {bot_link}'
    )


@global_handlers_router.message(StateFilter('ref_program_menu'), F.text)
async def answer_on_spam_handler(message: Message, state: FSMContext):
    await message.answer(
        text='Неизвестная команда.\n\n'
             'Выберите действие:',
        reply_markup=ref_program_menu()
    )
