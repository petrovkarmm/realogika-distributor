from aiogram.fsm.state import StatesGroup, State


class ShopDialog(StatesGroup):
    shop_dialog_menu = State()
    shop_item_detail = State()
    shop_item_buy_accepting = State()

    shop_promo_item_detail = State()
