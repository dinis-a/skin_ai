import os

from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

PAYMENT_PROVIDER_TOKEN = os.getenv('PAYMENT_PROVIDER_TOKEN', '')


async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='💳 Поддержка проекта через Telegram бот',
        description='📌 РАБОТАЕТ В ТЕСТОВОМ РЕЖИМЕ\nЕсли хотите поддержать проект, то можете внизу нажать на кнопку "Поддержать проект" и перевести любую сумму.',
        payload='Payment through a bot',
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency='rub',
        prices=[
            LabeledPrice(
                label='Плюс к карме 😊',
                amount=9900
            ),

            LabeledPrice(
                label='Скидка',
                amount=-2000
            )

        ],
        max_tip_amount=5000000,
        suggested_tip_amounts=[1000, 5000, 10000, 50000],
        start_parameter='Skin_AI',
        provider_data=None,
        photo_url='https://i.ibb.co/XZntMYY/android-chrome-512x512.png',
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=15
    )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(message: Message):
    msg = f'Спасибо за оплату {message.successful_payment.total_amount // 100} {message.successful_payment.currency}.'
    await message.answer(msg)
