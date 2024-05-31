from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram_bot.routers.start_command_router.keyboards import ref_code_no_roles_keyboard

ref_code_no_roles_router = Router()


@ref_code_no_roles_router.message(StateFilter('ref_code_no_roles'), F.text == 'Магазин')
async def open_shop_ref_code_no_roles(message: Message, state: FSMContext):
    await message.answer(
        text='Открытие магазина'
    )


@ref_code_no_roles_router.message(StateFilter('ref_code_no_roles'), F.text)
async def answer_on_spam_from_ref_code_no_roles(message: Message, state: FSMContext):
    await message.answer(
        text='Чтобы воспользоваться ботом, вам необходимо купить доступ в магазине.',
        reply_markup=ref_code_no_roles_keyboard()
    )