from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def close_invoice():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Отменить покупку')

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )