from aiogram import types

from filters import AdminCheck
from loader import dp, teachers


@dp.message_handler(AdminCheck(), commands=['clear_finalists'])
async def clear_finalists(message: types.Message):
    await teachers.clear_finalists()
    await message.reply('Готово')
