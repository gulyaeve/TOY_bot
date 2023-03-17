from aiogram import types

from loader import bot


async def set_default_commands():
    """
    Установка команд для бота (кнопка "Меню")
    """
    return await bot.set_my_commands([
        types.BotCommand(command="/start", description="Начать работу с чат-ботом"),
        types.BotCommand(command="/teachers", description="Список учителей"),
        types.BotCommand(command="/help", description="Помощь по командам чат-бота"),
        types.BotCommand(command="/cancel", description="Отмена текущего действия"),
    ])
