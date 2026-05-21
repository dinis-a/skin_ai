from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Мы в App Store', url='https://apps.apple.com/👨‍💻[В_РАЗРАБОТКЕ]')
    keyboard_builder.button(text='Мы в Google Play', url='https://play.google.com/store/👨‍💻[В_РАЗРАБОТКЕ]')
    keyboard_builder.button(text='Написать разработчикам', url='https://t.me/dinis_n')

    keyboard_builder.adjust(1, 1)
    return keyboard_builder.as_markup()
