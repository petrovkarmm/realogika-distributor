from pprint import pprint
from typing import Any

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Column, Select, Back, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from routers.global_utils.balance_dialog.balance_dataclass import RewardMovement, REWARD_KEY
from routers.global_utils.balance_dialog.balance_dialog_fetchers import get_all_user_rewards, \
    get_user_reward
from routers.global_utils.balance_dialog.balance_dialog_states import BalanceDialog
from routers.global_utils.balance_dialog.utils import convert_datetime
from routers.global_utils.keyboards import ref_program_menu
from routers.start_command.keyboards import ref_code_keyboard


async def tech_work(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await cq.answer(
        text='Временно недоступно.'
    )


async def close_dialog(callback: CallbackQuery,
                       button: Button,
                       dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except Exception as e:
        print(e)
        pass


def reward_movement_id_getter(reward_movement: RewardMovement) -> int:
    return reward_movement.id


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


async def on_reward_movement_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        reward_id_selected: int,
):
    reward_detail = await get_user_reward(reward_id_selected)
    dialog_manager.dialog_data['amount'] = reward_detail['amount']
    dialog_manager.dialog_data['comment'] = reward_detail['comment']
    dialog_manager.dialog_data['reward_date'] = convert_datetime(reward_detail['created_at'])
    dialog_manager.dialog_data['coefficient'] = reward_detail['koeff']
    dialog_manager.dialog_data['payment_date'] = convert_datetime(reward_detail['payment']['created_at'])
    dialog_manager.dialog_data['payment_amount'] = reward_detail['payment']['amount']

    await dialog_manager.switch_to(
        BalanceDialog.reward_detail
    )


async def user_balance_getter(**_kwargs):
    dialog_manager = _kwargs['dialog_manager']
    dialog_manager: DialogManager

    user_account_id = dialog_manager.start_data
    user_rewards_data = await get_all_user_rewards(user_account_id)

    if user_rewards_data:

        all_replenishments = 0

        for reward in user_rewards_data:
            all_replenishments += reward['amount']

        return {'all_replenishments': all_replenishments}

    else:
        return {'all_replenishments': 0}


async def user_balance_movement_getter(**_kwargs):
    dialog_manager = _kwargs['dialog_manager']
    dialog_manager: DialogManager

    user_account_id = dialog_manager.start_data
    user_rewards_data = await get_all_user_rewards(user_account_id)

    return {
        REWARD_KEY:
            [
                RewardMovement(reward['id'],
                               RewardMovement.format_amount(reward['amount']))
                for reward in user_rewards_data
            ]
    }


balance_menu_window = Window(
    Format(
        # "Текущий баланс: {dialog_data[current_balance]}"
        "\nВсего заработано: {all_replenishments} руб.",
        # "\nВсего выведено: {dialog_data[all_write_offs]}",
    ),
    SwitchTo(
        text=Const('Мои вознаграждения'), id='my_rewards', state=BalanceDialog.user_rewards
    ),
    # SwitchTo(
    #     text=Const('Пополнения/Списания'), id='balance_movement', state=BalanceDialog.money_movement
    # ),
    Button(
        text=Const("Вывод вознаграждений"), id="tech_work", on_click=tech_work
    ),
    Button(
        text=Const("Выйти"), id="back_to_menu", on_click=quit_from_balance
    ),
    state=BalanceDialog.balance_dialog_menu,
    getter=user_balance_getter
)

user_rewards_menu = Window(
    Format(
        "Выберите интересующее вознаграждение:"
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format("{item.amount}"),
                id="rewards_group",
                items=REWARD_KEY,
                item_id_getter=reward_movement_id_getter,
                on_click=on_reward_movement_selected,

            ),
        ),
        width=1,
        height=5,
        id="scroll_executors_menu",
        hide_on_single_page=True
    ),
    SwitchTo(
        text=Const('Назад'), id='back_to_balance', state=BalanceDialog.balance_dialog_menu
    ),
    Button(
        text=Const("Выйти"), id="back_to_menu", on_click=quit_from_balance
    ),
    getter=user_balance_movement_getter,
    state=BalanceDialog.user_rewards
)

reward_detail_window = Window(
    Format(
        "Сумма вознаграждения: +{dialog_data[amount]} руб.\n"
        "Дата получения вознаграждения: {dialog_data[reward_date]}\n"
        "Ваш коэффициент: {dialog_data[coefficient]}\n"
        "Комментарий: {dialog_data[comment]}\n\n"
        "Сумма покупки: {dialog_data[payment_amount]} руб.\n"
        "Дата покупки: {dialog_data[payment_date]}\n"
    ),
    SwitchTo(
        text=Const("Назад"), id="back", state=BalanceDialog.user_rewards
    ),
    Button(
        text=Const("Выйти"), id="back_to_menu", on_click=quit_from_balance
    ),
    state=BalanceDialog.reward_detail
)

balance_dialog = Dialog(
    balance_menu_window,
    reward_detail_window,
    user_rewards_menu
)
