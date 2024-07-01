from typing import Any

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Column, Select, Back, Row
from aiogram_dialog.widgets.text import Const, Format

from telegram_bot.routers.global_utils.shop_dialog.shop_dialog_states import ShopDialog
from telegram_bot.routers.global_utils.shop_dialog.shop_items_dataclass import ShopItem, SHOP_KEY
from telegram_bot.routers.ref_program.balance_dialog.balance_dataclass import BalanceMovement, BALANCE_KEY
from telegram_bot.routers.ref_program.balance_dialog.balance_dialog_states import BalanceDialog
from data_for_tests import test_user_balance_movement_data, \
    test_full_balance_movement_info, shop_main_page_data_test, test_shop_item_details
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


async def quit_from_shop(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    middleware_data = dialog_manager.middleware_data
    state = middleware_data['state']
    state: FSMContext

    # current_state = dialog_manager.start_data['current_state']

    await dialog_manager.done()

    # await state.set_state(
    #     current_state
    # )

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
    shop_item_detail_info = test_shop_item_details[int(shop_item_id)]

    item_count = shop_item_detail_info['count']
    if item_count <= 0:
        await callback.answer(
            text='Товар отсутствует.'
        )
    else:
        dialog_manager.dialog_data['name'] = shop_item_detail_info['name']
        dialog_manager.dialog_data['count'] = item_count
        dialog_manager.dialog_data['price'] = shop_item_detail_info['price']
        dialog_manager.dialog_data['description'] = shop_item_detail_info['description']

        await dialog_manager.switch_to(
            ShopDialog.shop_item_detail
        )


async def shop_items_getter(**_kwargs):
    dialog_manager = _kwargs['dialog_manager']

    if shop_main_page_data_test:
        dialog_manager.dialog_data['flag'] = True

    return {
        SHOP_KEY:
            [
                ShopItem(id=item['id'],
                         name=ShopItem.counter_checker(name=item['name'], count=item['count'])
                         )
                for item in shop_main_page_data_test
            ]
    }

shop_menu_window = Window(
    Const(
        "На текущий момент магазин пуст.",
        when=~F['dialog_data']
    ),
    Format(
        "Выберите интересующий вас продукт:",
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
        text=Const("Выйти"), id="quit_from_shop", on_click=quit_from_shop
    ),
    getter=shop_items_getter,
    state=ShopDialog.shop_dialog_menu
)

# dialog_manager.dialog_data['name'] = shop_item_detail_info['name']
# dialog_manager.dialog_data['count'] = shop_item_detail_info['count']
# dialog_manager.dialog_data['price'] = shop_item_detail_info['price']
# dialog_manager.dialog_data['description'] = shop_item_detail_info['description']

shop_item_detail_window = Window(
    Format(
        "Название товара: {dialog_data[name]}."
        "\nЦена: {dialog_data[price]} руб."
        "\nОписание: {dialog_data[description]}",
    ),
    Button(
      text=Const('Купить'), id='buy_item', on_click=None
    ),
    Row(
        Button(
            text=Const("Назад"), id="back", on_click=Back()
        ),
        Button(
            text=Const("Выйти"), id="quit_from_shop", on_click=quit_from_shop
        ),
    ),

    state=ShopDialog.shop_item_detail
)

shop_dialog = Dialog(
    shop_menu_window,
    shop_item_detail_window
)
