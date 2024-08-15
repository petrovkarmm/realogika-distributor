from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from routers.ref_code_no_roles.keyboards import ref_program_menu_keyboards
from routers.start_command.keyboards import ref_code_no_roles_keyboard

ref_code_no_roles_router = Router()


@ref_code_no_roles_router.message(StateFilter('ref_code_no_roles'), F.text == 'Реф. программа')
async def go_to_ref_program_router(message: Message, state: FSMContext):
    await message.answer(
        text='Кнопка реф. программа',
        reply_markup=ref_program_menu_keyboards()
    )
    await state.set_state(
        'ref_program_menu'
    )


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
