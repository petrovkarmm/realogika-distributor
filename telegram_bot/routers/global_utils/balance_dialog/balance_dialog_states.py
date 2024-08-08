from aiogram.fsm.state import StatesGroup, State


class BalanceDialog(StatesGroup):
    balance_dialog_menu = State()

    user_rewards = State()
    reward_detail = State()

    money_movement = State()
