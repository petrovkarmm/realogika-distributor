from aiogram import Router, F
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram_bot.routers.global_utils.func_utils import split_name_id_promocode
from telegram_bot.routers.start_command.keyboards import ref_code_no_roles_keyboard, ref_code_keyboard, \
    only_ref_program_keyboard

start_command_router = Router()


@start_command_router.message(StateFilter(None), Command('start'))
async def getting_start_with_new_users(message: Message, state: FSMContext, command: CommandObject):
    command_args = command.args

    if command_args:
        promocode_id, promocode_name = await split_name_id_promocode(command_args)

        if promocode_id and promocode_name:
            print('два значения')
        else:
            print('что-то не то.')

        await message.answer(
            text='Промокод успешно применён!',
            reply_markup=only_ref_program_keyboard()
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
