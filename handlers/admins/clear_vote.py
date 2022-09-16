from aiogram import types

from filters import AdminCheck
from loader import dp, teachers


@dp.message_handler(AdminCheck(), commands=['clear_votes'])
async def clear_votes(message: types.Message):
    await teachers.clear_votes()
    await message.answer('Голоса очищены')
