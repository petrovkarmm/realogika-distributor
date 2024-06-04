from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from telegram_bot.routers.ref_program.balance_dialog.balance_dialog_states import BalanceDialog

ref_program_router = Router()


@ref_program_router.message(StateFilter('ref_program_menu'), F.text == 'Баланс')
async def open_balance_dialog_handler(message: Message, state: FSMContext, dialog_manager: DialogManager):
    """
    Открытие диалога c балансом
    :param message:
    :param state:
    :return:
    """
    dialog_start_data = {

    }

    await dialog_manager.start(
        state=BalanceDialog.balance_dialog_menu,
        data=dialog_start_data
    )


@ref_program_router.message(StateFilter('ref_program_menu'), F.text == 'Моя структура')
async def open_my_arch_handler(message: Message, state: FSMContext):
    pass


@ref_program_router.message(StateFilter('ref_program_menu'), F.text == 'Моя реф. ссылка')
async def open_my_ref_link(message: Message, state: FSMContext):
    await message.answer(
        text='Ваша ссылка: {bot_link}'
    )
