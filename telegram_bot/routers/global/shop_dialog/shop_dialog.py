from typing import Any

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Column, Select, Back
from aiogram_dialog.widgets.text import Const, Format

from shop_items_dataclass import SHOP_KEY, ShopItem
from telegram_bot.routers.ref_program.balance_dialog.balance_dataclass import BalanceMovement, BALANCE_KEY
from telegram_bot.routers.ref_program.balance_dialog.balance_dialog_states import BalanceDialog
from data_for_tests import test_user_balance_movement_data, \
    test_full_balance_movement_info, shop_main_page_data_test
from telegram_bot.routers.start_command.keyboards import ref_code_keyboard


async def close_dialog(callback: CallbackQuery,
                       button: Button,
                       dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except Exception as e:
        print(e)
        pass


def shop_item_id_getter(shop_item: ShopItem) -> int:
    return shop_item.id


async def quit_from_balance(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    middleware_data = dialog_manager.middleware_data
    state = middleware_data['state']
    state: FSMContext

    current_state = dialog_manager.start_data['current_state']

    await dialog_manager.done()

    await state.set_state(
        current_state
    )

    # Нужно добавить функцию которая на основе current_state выдает нужную клаву.

    await cq.message.answer(
        text='Выберите действие:',
        reply_markup=ref_code_keyboard()
    )


async def on_shop_item_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        shop_item_id: int,
):
    shop_item_detail_info = shop_main_page_data_test[int(shop_item_id)]
    dialog_manager.dialog_data['name'] = shop_item_detail_info['name']
    dialog_manager.dialog_data['count'] = shop_item_detail_info['count']
    dialog_manager.dialog_data['price'] = shop_item_detail_info['price']
    dialog_manager.dialog_data['description'] = shop_item_detail_info['description']

    await dialog_manager.switch_to(
        BalanceDialog.balance_movement_detail
    )


async def shop_items_getter(**_kwargs):
    dialog_manager = _kwargs['dialog_manager']

    return {
        SHOP_KEY:
            [
                ShopItem(id=item['id'],
                         name=item['name'],
                         count=item['count'],
                         price=item['price'],
                         description=item['description'])
                for item in shop_main_page_data_test
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

shop_menu_window = Window(
    Const(
        "На текущий момент магазин пуст.",
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
                text=Format("{item.name}"),
                id="shop_item_select",
                items=SHOP_KEY,
                item_id_getter=shop_item_id_getter,
                on_click=on_shop_item_selected,
            ),
        ),
        width=1,
        height=5,
        id="scroll_executors_menu",
        when=F['dialog_data'],
        hide_on_single_page=True
    ),
    Button(
        text=Const("Выйти"), id="back_to_menu", on_click=quit_from_balance
    ),
    getter=shop_items_getter,
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

shop_dialog = Dialog(
    balance_menu_window,
    balance_movement_detail_window
)
