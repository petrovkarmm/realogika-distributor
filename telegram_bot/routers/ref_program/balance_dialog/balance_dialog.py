from typing import Any

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import SwitchTo, Row, Button, ScrollingGroup, Column, Select
from aiogram_dialog.widgets.text import Const, Format

from telegram_bot.routers.ref_program.balance_dialog.balance_dataclass import BalanceMovement, BALANCE_KEY
from telegram_bot.routers.ref_program.balance_dialog.balance_dialog_states import BalanceDialog


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


async def on_balance_movement_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        balance_movement_id: int,
):
    await callback.answer(
        text=str(balance_movement_id)
    )


async def user_balance_movement_getter(**_kwargs):
    dialog_manager = _kwargs['dialog_manager']

    dialog_manager.dialog_data['current_balance'] = 12346
    dialog_manager.dialog_data['all_replenishments'] = 100000
    dialog_manager.dialog_data['all_write_offs'] = 20000

    test_data = [
        {
            'id': 1,
            'amount': 100,
            'is_accrual': True
        },
        {
            'id': 2,
            'amount': 12,
            'is_accrual': False
        },
        {
            'id': 3,
            'amount': 220,
            'is_accrual': True
        },
        {
            'id': 4,
            'amount': 4000,
            'is_accrual': False
        },
        {
            'id': 5,
            'amount': 56,
            'is_accrual': True
        },
    ]

    return {
        BALANCE_KEY:
            [
                BalanceMovement(balance_movement['id'],
                                BalanceMovement.format_amount(balance_movement['amount'],
                                                              balance_movement['is_accrual']))
                for balance_movement in test_data
            ]
    }


# balance_menu = Window(
#     Const("Добро пожаловать в меню CRM бота.\n\n"
#           "Выберите действие: "),
#     SwitchTo(
#         text=Const("➕ Создать задачу"), id="make_task",
#         # when=is_admin
#     ),
#     Row(
#         SwitchTo(
#             text=Const("📥 Задачи для меня"), id="my_tasks", state=DialogTaskMenu.my_tasks
#         ),
#         SwitchTo(
#             text=Const("✉️ Задачи от меня"), id="my_orders", state=DialogTaskMenu.my_orders
#         )
#     ),
#     Button(
#         text=Const("🔚 Выйти"), id="close_dialog", on_click=close_dialog
#     ),
#     state=state=BalanceDialog.balance_dialog_menu
# )

# Баланс - выводим список его последних 20 начислений/списаний.
# И ниже три подсчитанных значения:
# Всего заработано: Сумма
# Всего выведено: Сумма
# Баланс: Сумма

# dialog_manager.dialog_data['current_balance'] = 12346
# dialog_manager.dialog_data['all_replenishments'] = 100000
# dialog_manager.dialog_data['all_write_offs'] = 20000

balance_menu = Window(
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
        text=Const("Выйти"), id="back_to_menu", on_click=None
    ),
    getter=user_balance_movement_getter,
    state=BalanceDialog.balance_dialog_menu
)

balance_dialog = Dialog(
    balance_menu
)
