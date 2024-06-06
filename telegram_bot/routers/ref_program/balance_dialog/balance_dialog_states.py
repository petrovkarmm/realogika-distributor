from aiogram.fsm.state import StatesGroup, State


class BalanceDialog(StatesGroup):
    balance_dialog_menu = State()
    balance_movement_detail = State()

