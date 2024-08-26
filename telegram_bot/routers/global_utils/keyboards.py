from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def close_invoice():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Отменить покупку')

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )


def ref_program_menu():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Мои рефералы')
    keyboard_builder.button(text='Баланс')
    keyboard_builder.button(text='Моя реф. ссылка')
    # keyboard_builder.button(text='Магазин')
    keyboard_builder.button(text='В меню')

    keyboard_builder.adjust(3)

    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
