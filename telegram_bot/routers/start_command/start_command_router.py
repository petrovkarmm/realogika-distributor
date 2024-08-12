from aiogram import Router, F
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram_bot.routers.global_utils.func_utils import split_name_id_promocode
from telegram_bot.routers.start_command.keyboards import ref_code_no_roles_keyboard, ref_code_keyboard, \
    only_ref_program_keyboard
from telegram_bot.routers.start_command.start_command_fetchers import patch_user_promocode

start_command_router = Router()


@start_command_router.message(StateFilter(None), Command('start'))
async def getting_start_with_new_users(message: Message, state: FSMContext, command: CommandObject):
    command_args = command.args

    if command_args:
        status_code, promocode_patch_response = await patch_user_promocode(promocode_name=command_args,
                                                                           telegram_user_id=message.from_user.id)

        if status_code == 200:
            promocode_data = promocode_patch_response['promocodes'][0]
            promocode_offer_id = promocode_data['offer_id']
            if promocode_offer_id:
                # логика перехода в магазин.
                pass
            await state.set_state(
                'ref_program_menu'
            )
            await message.answer(
                text='Промокод успешно применён!',
                reply_markup=only_ref_program_keyboard()
            )
        elif status_code == 404:
            await message.answer(
                text='Промокод не найден.'
            )
        elif status_code == 422:
            await state.set_state(
                'ref_program_menu'
            )
            await message.answer(
                text='За вами уже закреплен промокод.',
                reply_markup=only_ref_program_keyboard()
            )
        else:
            await message.answer(
                text='На сервере технические неполадки.\n'
                     'Пожалуйста, повторите позже.'
            )
    else:
        await message.answer(
            text='Добро пожаловать в бота дистрибьютора Релогики!\n'
                 'Чтобы воспользоваться ботом необходимо использовать ссылку приглашение.',
        )


@start_command_router.message(StateFilter(None), F.text)
async def answer_on_spam_from_none(message: Message, state: FSMContext):
    await message.answer(
        text='Добро пожаловать в бота дистрибьютора Релогики!\n'
             'Чтобы воспользоваться ботом необходимо использовать ссылку приглашение.',
    )
