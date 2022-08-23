from handlers.admins.admins import notify_admins
from loader import bot, storage, dp, db
import filters, middlewares, handlers
from aiogram import executor

from utils.commands import set_default_commands
from utils.messages.create_messages import create_messages
from utils.parameters.create_parameters import create_parameters
from utils.users.create_user_types import create_user_types
from utils.utilities import get_bot_info, make_dict_output


async def on_shutdown(dp):
    await bot.delete_my_commands()
    # await notify_admins("Бот выключен...")
    await storage.close()
    await bot.close()


async def on_startup(dp):
    await set_default_commands()
    bot_info = make_dict_output(await get_bot_info())
    await create_user_types()
    await create_messages()
    await create_parameters()
    await notify_admins(f"Бот запущен и готов к работе.\n\n<code>{bot_info}</code>")


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)
