from pprint import pprint
from typing import Any

from aiogram import F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, Chat
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Column, Select, Back, Row, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia, StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from data_for_tests import test_data_list, detail_item_test_data
from telegram_bot.routers.global_utils.func_utils import uuid_generation
from telegram_bot.routers.global_utils.keyboards import close_invoice, ref_program_menu
from telegram_bot.routers.global_utils.shop_dialog.shop_dialog_fetchers import get_all_items_from_shop, \
    get_item_from_shop, post_create_payment
from telegram_bot.routers.global_utils.shop_dialog.shop_dialog_states import ShopDialog
from telegram_bot.routers.global_utils.shop_dialog.shop_items_dataclass import ShopItem, SHOP_KEY
from telegram_bot.routers.global_utils.shop_dialog.utils import validate_image_url
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


async def promo_item_data_getter(**_kwargs):
    dialog_manager = _kwargs['dialog_manager']
    dialog_manager: DialogManager
    dialog_manager_middleware_object = dialog_manager.middleware_data

    state_object = dialog_manager_middleware_object['state']
    state_object: FSMContext

    shop_item_id = dialog_manager.start_data

    shop_item_detail_info = await get_item_from_shop(shop_item_id)
    # shop_item_detail_info = detail_item_test_data.get(int(shop_item_id))

    text_after_payment = shop_item_detail_info['offers'][0]['text_after_payment']
    url_image = validate_image_url(shop_item_detail_info['offers'][0]['url_image'])

    promo_item_title = shop_item_detail_info['title']
    promo_item_id = shop_item_detail_info['id']
    promo_item_price = shop_item_detail_info['offers'][0]['price']
    promo_item_url_image = url_image
    promo_item_description = shop_item_detail_info['offers'][0]['description']

    dialog_manager.dialog_data['title'] = promo_item_title
    dialog_manager.dialog_data['id'] = promo_item_id
    dialog_manager.dialog_data['price'] = promo_item_price
    dialog_manager.dialog_data['url_image'] = promo_item_url_image
    dialog_manager.dialog_data['description'] = promo_item_description

    await state_object.update_data(
        text_after_payment=text_after_payment
    )

    return {
        'promo_item_title': promo_item_title,
        'promo_item_id': promo_item_id,
        'promo_item_price': promo_item_price,
        'promo_item_url_image': promo_item_url_image,
        'promo_item_description': promo_item_description
    }


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
    current_shop_item_id = dialog_manager.dialog_data['id']

    # TODO

    # current_shop_item_price = 10000  # ДЛЯ ТЕСТОВ ПОТОМ УБРАТЬ!

    prices = [
        LabeledPrice(label="Цена", amount=current_shop_item_price),
    ]

    provider_token = '381764678:TEST:89271'
    currency = 'RUB'
    payload = await uuid_generation()

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

    payment_data = {
        "payload": payload,
        "user_tg_id": callback_query.message.from_user.id,
        "offer_id": current_shop_item_id,
        "amount": current_shop_item_price
    }

    await post_create_payment(payment_data)

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
        invoice_object=invoice_object,
        current_shop_item_id=current_shop_item_id,
        current_payload=payload
    )


async def go_to_item_buy_accepting(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.switch_to(
        ShopDialog.shop_item_buy_accepting
    )


async def get_item_free(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    current_shop_item_id = dialog_manager.dialog_data['id']
    current_user_id = callback.message.from_user.id
    await callback.message.answer(
        text=f'Testing user_id and shop_item_id:\n'
             f'User_id: {current_user_id}\n '
             f'Shop_item_id: {current_shop_item_id}'
    )

    await dialog_manager.switch_to(
        ShopDialog.shop_dialog_menu
    )


async def quit_from_shop(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    middleware_data = dialog_manager.middleware_data
    state = middleware_data['state']
    state: FSMContext

    # TODO

    # current_state = dialog_manager.start_data['current_state']

    await dialog_manager.done()

    # await state.set_state(
    #     current_state
    # )

    # Нужно добавить функцию которая на основе current_state выдает нужную клаву.

    await callback.message.answer(
        text='Выберите действие:',
        reply_markup=ref_program_menu()
    )


async def on_shop_item_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        shop_item_id: int,
):
    dialog_manager_middleware_object = dialog_manager.middleware_data

    state_object = dialog_manager_middleware_object['state']
    state_object: FSMContext

    shop_item_detail_info = await get_item_from_shop(shop_item_id)
    # shop_item_detail_info = detail_item_test_data.get(int(shop_item_id))

    text_after_payment = shop_item_detail_info['offers'][0]['text_after_payment']
    url_image = validate_image_url(shop_item_detail_info['offers'][0]['url_image'])

    dialog_manager.dialog_data['title'] = shop_item_detail_info['title']
    dialog_manager.dialog_data['id'] = shop_item_detail_info['id']
    dialog_manager.dialog_data['price'] = shop_item_detail_info['offers'][0]['price']
    dialog_manager.dialog_data['url_image'] = url_image
    dialog_manager.dialog_data['description'] = shop_item_detail_info['offers'][0]['description']

    await state_object.update_data(
        text_after_payment=text_after_payment
    )

    await dialog_manager.switch_to(
        ShopDialog.shop_item_detail
    )


async def shop_items_getter(**_kwargs):
    dialog_manager = _kwargs['dialog_manager']
    event_chat = _kwargs['event_chat']
    event_chat: Chat
    user_id = event_chat.id

    shop_items_object = await get_all_items_from_shop(user_id)
    # shop_items_object = test_data_list

    if shop_items_object:
        dialog_manager.dialog_data['flag'] = True

    return {
        SHOP_KEY:
            [
                ShopItem(id=item['id'], title=item['title'])
                for item in shop_items_object
                # if item['available'] раскомитить после добавления поля в бд

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

promo_item_detail_window = Window(
    Format(
        "Название товара: {promo_item_title}\n"
        "Цена: {promo_item_price}\n"
        "Описание: {promo_item_description}"
    ),
    Button(
      text=Format('Купить'), id='go_to_buy_item', on_click=go_to_item_buy_accepting
    ),
    StaticMedia(
        url=Format('promo_item_url_image')
    ),
    Row(
        SwitchTo(
            text=Const('В магазин'), id='to_shop', state=ShopDialog.shop_dialog_menu
        ),
        Button(
            text=Const("Выйти"), id="quit_from_shop", on_click=quit_from_shop
        )
    ),
    state=ShopDialog.shop_promo_item_detail,
    getter=promo_item_data_getter
)

shop_item_detail_window = Window(
    Format(
        "Название товара: {dialog_data[title]}."
        "\nЦена: {dialog_data[price]} руб."
        "\nОписание: {dialog_data[description]}",
        when=F['dialog_data']['price'] > 0
    ),
    Format(
        "Название товара: {dialog_data[title]}."
        "\nЦена: Бесплатно"
        "\nОписание: {dialog_data[description]}",
        when=F['dialog_data']['price'] == 0
    ),
    Button(
        text=Format('Купить'), id='go_to_buy_item', on_click=go_to_item_buy_accepting,
        when=F['dialog_data']['price'] > 0
    ),
    Button(
        text=Format('Получить'), id='get_item_free', on_click=get_item_free,
        when=F['dialog_data']['price'] == 0
    ),
    StaticMedia(
        url=Format('{dialog_data[url_image]}')
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
        "Цена: {dialog_data[price]} рублей",
        when=F['dialog_data']['price'] > 0
    ),
    Format(
        "Пожалуйста, подтвердите покупку.\n\n"
        "{dialog_data[title]}\n"
        "Цена: Бесплатно",
        when=F['dialog_data']['price'] == 0
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
    state=ShopDialog.shop_item_buy_accepting,
)

shop_dialog = Dialog(
    shop_menu_window,
    shop_item_detail_window,
    shop_item_buy_accepting_window
)
