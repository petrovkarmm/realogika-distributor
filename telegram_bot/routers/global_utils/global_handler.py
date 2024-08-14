import asyncio
from pprint import pprint

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from telegram_bot.routers.global_utils.balance_dialog.balance_dialog_states import BalanceDialog
from telegram_bot.routers.global_utils.balance_dialog.utils import convert_datetime
from telegram_bot.routers.global_utils.global_fetchers import get_my_sponsor_data, get_my_sponsored_users_data, \
    get_user_data, get_user_promocode
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

    await state.set_state(
        'ref_program_menu'
    )

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

    user_account_data = await get_user_data(message.from_user.id)
    user_account_id = user_account_data['account']['id']

    sponsor_data = await get_my_sponsor_data(user_account_id)
    if sponsor_data:
        sponsor_name = sponsor_data[0]['sponsor']['first_name'] or 'отсутствует.'
        sponsor_last_name = sponsor_data[0]['sponsor']['last_name'] or 'отсутствует.'
        sponsor_email = sponsor_data[0]['sponsor']['email'] or 'отсутствует.'

        promocode_data = user_account_data['promocodes'][0]
        promocode_data_end_date = promocode_data['end_at']
        promocode_data_end_date_convert = convert_datetime(promocode_data_end_date)

        await message.answer(
            text='Дата окончания промокода:\n\n'
                 f'{promocode_data_end_date_convert}\n\n'
                 'Данные вашего спонсора:\n\n'
                 f'Имя - {sponsor_name}\n'
                 f'Фамилия - {sponsor_last_name}\n'
                 f'Email - {sponsor_email}',
            reply_markup=ref_program_menu()
        )

    else:
        await message.answer(
            text='У вас отсутствует спонсор.',
            reply_markup=ref_program_menu()
        ),


@global_handlers_router.message(StateFilter('ref_program_menu'), F.text == 'Баланс')
async def open_balance_dialog_handler(message: Message, state: FSMContext, dialog_manager: DialogManager):
    """
    Открытие диалога с балансом
    :param message:
    :param state:
    :param dialog_manager:
    :return:
    """
    user_account_data = await get_user_data(message.from_user.id)
    user_account_id = user_account_data['account']['id']

    await message.answer(
        text='Выберите интересующий тип движения:',
        reply_markup=types.ReplyKeyboardRemove()
    )

    await dialog_manager.start(
        state=BalanceDialog.balance_dialog_menu,
        data=user_account_id
    )


@global_handlers_router.message(StateFilter('ref_program_menu'), F.text == 'Мои рефералы')
async def open_my_arch_handler(message: Message, state: FSMContext):
    user_account_data = await get_user_data(message.from_user.id)
    user_account_id = user_account_data['account']['id']

    sponsored_users_data = await get_my_sponsored_users_data(user_account_id)

    if sponsored_users_data:
        sponsored_users_result_answer = ('Ваши рефералы:\n\n'
                                         '----------------')

        for sponsored_user in sponsored_users_data:
            sponsored_user_object = sponsored_user['user']
            sponsored_user_first_name = sponsored_user_object['first_name'] or 'отсутствует.'
            if sponsored_user_object['users'][0]['username']:
                sponsored_user_link = f'@{sponsored_user_object["users"][0]["username"]}'
            else:
                sponsored_user_link = 'отсутствует.'
            sponsored_users_result_answer += (f'\nИмя - {sponsored_user_first_name}\n'
                                              f'Ссылка - {sponsored_user_link}\n----------------')
        await message.answer(
            text=sponsored_users_result_answer,
            reply_markup=ref_program_menu()
        )
    else:
        await message.answer(
            text='У вас отсутствуют рефералы.',
            reply_markup=ref_program_menu()
        )


@global_handlers_router.message(StateFilter('ref_program_menu'), F.text == 'Моя реф. ссылка')
async def open_my_ref_link(message: Message, state: FSMContext):
    user_promocode_data = await get_user_promocode(message.from_user.id)
    try:
        ref_link_code = user_promocode_data[0]['code']
    except KeyError:
        await message.answer(
            text=f'{user_promocode_data["detail"]}'
        )
    else:
        await message.answer(
            text='Ваша реферальная ссылка:\n\n'
                 f'https://t.me/ReDister_bot?start={ref_link_code}'
        )


@global_handlers_router.message(StateFilter('ref_program_menu'), F.text)
async def answer_on_spam_handler(message: Message, state: FSMContext):
    await message.answer(
        text='Неизвестная команда.\n\n'
             'Выберите действие:',
        reply_markup=ref_program_menu()
    )
