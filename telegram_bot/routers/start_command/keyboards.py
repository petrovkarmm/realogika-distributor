from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def ref_code_no_roles_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Магазин')
    keyboard_builder.button(text='Реф. программа')

    keyboard_builder.adjust(2)

    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )


def ref_code_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Магазин')
    keyboard_builder.button(text='Реф. программа')
    keyboard_builder.button(text='Баланс')

    keyboard_builder.adjust(2)

    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
