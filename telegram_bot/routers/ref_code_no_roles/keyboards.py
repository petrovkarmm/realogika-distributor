from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def ref_program_menu_keyboards():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Магазин')
    keyboard_builder.button(text='Моя структура')
    keyboard_builder.button(text='Баланс')
    keyboard_builder.button(text='Моя реф. ссылка')

    keyboard_builder.adjust(2)

    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
