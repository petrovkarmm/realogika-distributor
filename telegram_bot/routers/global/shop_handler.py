from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from telegram_bot.routers.global_utils.shop_dialog.shop_dialog_states import ShopDialog

global_handlers_router = Router()


@global_handlers_router.message(F.text == 'Магазин')
async def global_shop_handler(message: Message, state: FSMContext, dialog_manager: DialogManager):
    """
    Запуск диалогового окна магазина с эквайрингом на оплату внутри.
    :param message:
    :param state:
    :return:
    """
    await message.answer(
        text='Выберите интересующий вас продукт:',
        reply_markup=types.ReplyKeyboardRemove()
    )

    await dialog_manager.start(
        state=ShopDialog.shop_dialog_menu
    )
