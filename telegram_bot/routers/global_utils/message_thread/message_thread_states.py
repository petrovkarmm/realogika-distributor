from aiogram.fsm.state import StatesGroup, State


class MessageThreadStates(StatesGroup):
    message_thread_menu = State()