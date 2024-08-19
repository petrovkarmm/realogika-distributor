from aiogram import Router, F
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from routers.global_utils.func_utils import split_name_id_promocode
from routers.global_utils.shop_dialog.shop_dialog_states import ShopDialog
from routers.start_command.keyboards import ref_code_no_roles_keyboard, ref_code_keyboard, \
    only_ref_program_keyboard
from routers.start_command.start_command_fetchers import patch_user_promocode, get_shop_item_id, \
    get_sponsor_user_data

from routers.global_utils.global_fetchers import get_user_data, get_my_sponsor_data

from routers.global_utils.keyboards import ref_program_menu

start_command_router = Router()


@start_command_router.message(StateFilter(None), Command('start'))
async def getting_start_with_new_users(message: Message, state: FSMContext, command: CommandObject,
                                       dialog_manager: DialogManager):
    command_args = command.args

    if command_args:

        sponsored_user_data = {
            "external_id": f"{message.from_user.id}",
            "username": f"{message.from_user.username}",
            "fullname": f"{message.from_user.full_name}",
            "account_data": {
                "first_name": f"{message.from_user.first_name}",
                "last_name": f"{message.from_user.last_name}",
            }
        }

        status_code, promocode_patch_response = await patch_user_promocode(promocode_name=command_args,
                                                                           telegram_user_id=message.from_user.id,
                                                                           sponsored_user_data=sponsored_user_data)

        if status_code == 200:
            promocode_data = promocode_patch_response['promocodes'][0]
            sponsor_account_id = promocode_data['account_id']
            sponsor_user_data = await get_sponsor_user_data(sponsor_account_id)

            sponsor_telegram_id = sponsor_user_data['users'][0]['external_id']

            sponsored_user_username = message.from_user.username
            if sponsored_user_username:
                sponsored_user_username = '@' + sponsored_user_username
            else:
                sponsored_user_username = 'Username отсутствует.'
            sponsored_user_first_name = message.from_user.first_name or 'Имя отсутствует.'
            sponsored_user_last_name = message.from_user.last_name or 'Фамилия отсутствует.'

            try:
                await message.bot.send_message(
                    text=f'Поздравляем! У вас появился новый реферал!\n'
                         f'Данные нового реферала:\n\n'
                         f'{sponsored_user_username}\n'
                         f'{sponsored_user_last_name}\n'
                         f'{sponsored_user_first_name}',
                    chat_id=sponsor_telegram_id
                )
            except Exception as e:
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
    user_account_data = await get_user_data(message.from_user.id)
    user_account_id = user_account_data['account']['id']

    sponsor_data = await get_my_sponsor_data(user_account_id)

    if sponsor_data:
        await state.set_state(
            'ref_program_menu'
        )
        await message.answer(
            text=('Произошла техничская ошибка.\n'
                  'Пожалуйста, повторите действие.'
                  ),
            reply_markup=ref_program_menu()
        )
    else:

        await message.answer(
            text='Добро пожаловать в бота дистрибьютора Релогики!\n'
                 'Чтобы воспользоваться ботом необходимо использовать ссылку приглашение.',
        )
