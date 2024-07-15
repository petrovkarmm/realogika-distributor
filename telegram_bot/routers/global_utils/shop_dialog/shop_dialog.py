from pprint import pprint
from typing import Any

from aiogram import F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Column, Select, Back, Row
from aiogram_dialog.widgets.text import Const, Format

from telegram_bot.routers.global_utils.keyboards import close_invoice
from telegram_bot.routers.global_utils.shop_dialog.shop_dialog_fetchers import get_all_items_from_shop, \
    get_item_from_shop
from telegram_bot.routers.global_utils.shop_dialog.shop_dialog_states import ShopDialog
from telegram_bot.routers.global_utils.shop_dialog.shop_items_dataclass import ShopItem, SHOP_KEY
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


async def send_invoice_click(
        callback_query: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    dialog_middleware_object = dialog_manager.middleware_data
    bot_object = dialog_middleware_object['bot']
    state_object = dialog_middleware_object['state']
    bot_object: Bot
    state_object: FSMContext

    current_chat_id = callback_query.message.chat.id

    current_shop_item_name = dialog_manager.dialog_data['title']
    current_shop_item_description = dialog_manager.dialog_data['description']
    current_shop_item_price = dialog_manager.dialog_data['price'] * 100

    prices = [
        LabeledPrice(label="Цена", amount=current_shop_item_price),
    ]

    shop_id = 506751
    shop_article_id = 538350

    provider_token = '381764678:TEST:89271'
    currency = 'RUB'
    payload = '381764678:TEST:89271'

    "botfather token 381764678:TEST:89271"
    "shopId 506751 shopArticleId 538350"
    "1111 1111 1111 1026, 12/22, CVC 000."

    # https://yookassa.ru/docs/support/payments/onboarding/integration/cms-module/telegram

    await callback_query.message.answer(
        text='*Оплатите покупку нажав кнопку ниже.\n'
             'Для отмены покупки нажмите кнопку под чатом.*',
        reply_markup=close_invoice(),
        parse_mode='Markdown'
    )

    await dialog_manager.done()

    await state_object.set_state(
        'on_invoice_payment'
    )

    invoice_object = await bot_object.send_invoice(
        chat_id=current_chat_id,
        title=current_shop_item_name,
        description=current_shop_item_description,
        currency=currency,
        provider_token=provider_token,
        payload=payload,
        prices=prices
    )

    await state_object.update_data(
        invoice_object=invoice_object
    )


async def go_to_item_buy_accepting(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.switch_to(
        ShopDialog.shop_item_buy_accepting
    )


async def quit_from_shop(
        callback: CallbackQuery,
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

    await callback.message.answer(
        text='Выберите действие:',
        reply_markup=ref_code_keyboard()
    )


async def on_shop_item_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        shop_item_id: int,
):
    shop_item_detail_info = await get_item_from_shop(shop_item_id)

    dialog_manager.dialog_data['title'] = shop_item_detail_info['title']
    dialog_manager.dialog_data['price'] = shop_item_detail_info['offers'][0]['price']
    dialog_manager.dialog_data['action'] = shop_item_detail_info['action']['name']
    dialog_manager.dialog_data['description'] = shop_item_detail_info['offers'][0]['description']

    await dialog_manager.switch_to(
        ShopDialog.shop_item_detail
    )


async def shop_items_getter(**_kwargs):
    dialog_manager = _kwargs['dialog_manager']

    shop_items_object = await get_all_items_from_shop()

    pprint(shop_items_object)

    if shop_items_object:
        dialog_manager.dialog_data['flag'] = True

    return {
        SHOP_KEY:
            [
                ShopItem(id=item['id'], title=item['title'])
                for item in shop_items_object
                # if item['available'] раскомитить после добавления боля в бд

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
                text=Format("{item.title}"),
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

shop_item_detail_window = Window(
    Format(
        "Название товара: {dialog_data[title]}."
        "\nЦена: {dialog_data[price]} руб."
        "\nОписание: {dialog_data[description]}",
    ),
    Button(
        text=Format('{dialog_data[action]}'), id='go_to_buy_item', on_click=go_to_item_buy_accepting
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

shop_item_buy_accepting_window = Window(
    Format(
        "Пожалуйста, подтвердите покупку.\n\n"
        "{dialog_data[title]}\n"
        "Цена: {dialog_data[price]} рублей"
    ),
    Button(
        text=Const("Подтверждаю"), id='buy_item', on_click=send_invoice_click
    ),
    Row(
        Button(
            text=Const("Назад"), id="back", on_click=Back()
        ),
        Button(
            text=Const("Выйти"), id="quit_from_shop", on_click=quit_from_shop
        ),
    ),
    state=ShopDialog.shop_item_buy_accepting
)

shop_dialog = Dialog(
    shop_menu_window,
    shop_item_detail_window,
    shop_item_buy_accepting_window
)
