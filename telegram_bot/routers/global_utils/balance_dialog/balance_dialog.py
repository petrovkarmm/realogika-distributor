from typing import Any

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Column, Select, Back
from aiogram_dialog.widgets.text import Const, Format

from telegram_bot.routers.global_utils.balance_dialog.balance_dataclass import BalanceMovement, BALANCE_KEY
from telegram_bot.routers.global_utils.balance_dialog.balance_dialog_states import BalanceDialog
from data_for_tests import test_user_balance_movement_data, \
    test_full_balance_movement_info
from telegram_bot.routers.global_utils.keyboards import ref_program_menu
from telegram_bot.routers.start_command.keyboards import ref_code_keyboard


async def close_dialog(callback: CallbackQuery,
                       button: Button,
                       dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except Exception as e:
        print(e)
        pass


def balance_movement_id_getter(balance_movement: BalanceMovement) -> int:
    return balance_movement.id


async def quit_from_balance(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    middleware_data = dialog_manager.middleware_data
    state = middleware_data['state']
    state: FSMContext

    await dialog_manager.done()

    # TODO

    # Нужно добавить функцию которая на основе current_state выдает нужную клаву.

    await state.set_state(
        'ref_program_menu'
    )
    await cq.message.answer(
        text='Выберите действие:',
        reply_markup=ref_program_menu()
    )


async def on_balance_movement_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        balance_movement_id: int,
):
    user_balance_movement_detail = test_full_balance_movement_info[int(balance_movement_id)]
    dialog_manager.dialog_data['amount'] = user_balance_movement_detail['amount']
    dialog_manager.dialog_data['is_accrual'] = user_balance_movement_detail['is_accrual']
    dialog_manager.dialog_data['date'] = user_balance_movement_detail['date']
    dialog_manager.dialog_data['info'] = user_balance_movement_detail['info']

    await dialog_manager.switch_to(
        BalanceDialog.balance_movement_detail
    )


async def user_balance_movement_getter(**_kwargs):
    dialog_manager = _kwargs['dialog_manager']

    dialog_manager.dialog_data['current_balance'] = 12346
    dialog_manager.dialog_data['all_replenishments'] = 100000
    dialog_manager.dialog_data['all_write_offs'] = 20000

    return {
        BALANCE_KEY:
            [
                BalanceMovement(balance_movement['id'],
                                BalanceMovement.format_amount(balance_movement['amount'],
                                                              balance_movement['is_accrual']))
                for balance_movement in test_user_balance_movement_data
            ]
    }


balance_menu_window = Window(
    Const(
        "У вас отсутствую движения по балансу.",
        when=~F['dialog_data']
    ),
    Format(
        "Текущий баланс: {dialog_data[current_balance]}"
        "\nВсего заработано: {dialog_data[all_replenishments]}"
        "\nВсего выведено: {dialog_data[all_write_offs]}",
        when=F['dialog_data']
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format("{item.amount}"),
                id="task_select",
                items=BALANCE_KEY,
                item_id_getter=balance_movement_id_getter,
                on_click=on_balance_movement_selected,
            ),
        ),
        width=1,
        height=5,
        id="scroll_executors_menu",
        when=F['dialog_data']
    ),
    Button(
        text=Const("Выйти"), id="back_to_menu", on_click=quit_from_balance
    ),
    getter=user_balance_movement_getter,
    state=BalanceDialog.balance_dialog_menu
)

balance_movement_detail_window = Window(
    Format(
        "Сумма пополнения:  +{dialog_data[amount]}руб."
        "\nДата пополнения: {dialog_data[date]}"
        "\nИнформация: {dialog_data[info]}",
        when=F['dialog_data']['is_accrual']
    ),
    Format(
        "Сумма списания:  -{dialog_data[amount]}руб."
        "\nДата списания: {dialog_data[date]}"
        "\nИнформация: {dialog_data[info]}",
        when=~F['dialog_data']['is_accrual']
    ),
    Button(
        text=Const("Назад"), id="back", on_click=Back()
    ),
    Button(
        text=Const("Выйти"), id="back_to_menu", on_click=quit_from_balance
    ),
    state=BalanceDialog.balance_movement_detail
)

balance_dialog = Dialog(
    balance_menu_window,
    balance_movement_detail_window
)
