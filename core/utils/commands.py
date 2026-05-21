from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):

    commands = [
        BotCommand(
            command='help',
            description='🆘 Помощь'
        ),
        BotCommand(
            command='cancel',
            description='🧹 Удалить все данные'
        ),
        BotCommand(
            command='inline',
            description='📱 Скачать приложение, связаться с разработчиками'
        ),
        BotCommand(
            command='pay',
            description='💰 Пожертвования проекту'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
