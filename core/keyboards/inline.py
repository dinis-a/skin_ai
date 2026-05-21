from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Написать разработчикам', url='https://t.me/dinis_n')
    return keyboard_builder.as_markup()
