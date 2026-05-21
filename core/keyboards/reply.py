from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='FAQ')
    keyboard_builder.button(text='Поддержать проект')
    keyboard_builder.button(text='Заказать бот')
    keyboard_builder.button(text='Помогите улучшить качество сервиса')
    keyboard_builder.adjust(3, 1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=False,
                               input_field_placeholder='⬇Помочь проекту, заказать бот⬇')
