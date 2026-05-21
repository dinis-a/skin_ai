import asyncio
import logging
import os
import warnings
from logging.handlers import TimedRotatingFileHandler

from aiogram import Bot, Dispatcher, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command

from core.handlers.basic import *  # noqa: F403
from core.handlers.basic import get_inline
from core.handlers.pay import order, pre_checkout_query, successful_payment
from core.settings import settings
from core.utils.commands import set_commands

warnings.filterwarnings("ignore")


async def start_bot(bot: Bot):
    await set_commands(bot)
    BotName = await bot.get_my_name()
    await bot.send_message(settings.bots.admin_id, text=f"Бот <b>{BotName.name}</b> запущен!", disable_notification=True)


async def stop_bot(bot: Bot):
    BotName = await bot.get_my_name()
    await bot.send_message(settings.bots.admin_id, text=f"Бот <b>{BotName.name}</b> выключен! Ведутся технические работы.", disable_notification=True)


async def start():
    os.makedirs('photos', exist_ok=True)
    os.makedirs('/app/logs', exist_ok=True)

    log_format = logging.Formatter("%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    file_handler = TimedRotatingFileHandler("/app/logs/skin_v2.log", when="midnight", interval=1, backupCount=3)
    file_handler.setFormatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(order, Command(commands='pay'))
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.message.register(successful_payment, F.content_type == 'SUCCESSFUL_PAYMENT')

    dp.message.register(get_newsletter, F.text.lower().count("#рассылка") > 0)
    dp.message.register(get_inline, Command(commands='inline'))
    dp.message.register(get_hello, F.text.lower() == 'привет')
    dp.message.register(get_smile, F.text.count('👍') > 0)
    dp.message.register(get_help, F.text == '/help')
    dp.message.register(get_cancel, F.text == '/cancel')
    dp.message.register(get_support, F.text == 'Поддержать проект')
    dp.message.register(get_order, F.text == 'Заказать бот')
    dp.message.register(get_faq, F.text == 'FAQ')
    dp.message.register(get_better, F.text == 'Помогите улучшить качество сервиса')
    dp.message.register(get_photo, F.photo)

    dp.message.register(get_start, Command(commands='start'))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
