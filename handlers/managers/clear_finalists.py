from aiogram import types

from filters import ManagerCheck
from loader import dp, teachers


@dp.message_handler(ManagerCheck(), commands=['clear_finalists'])
async def clear_finalists(message: types.Message):
    await teachers.clear_finalists()
    await message.reply('Готово')
