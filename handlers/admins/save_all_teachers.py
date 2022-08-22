
from aiogram import types

from filters import AdminCheck
from loader import dp, teachers
from utils.teachers.create_teachers import create_teachers


@dp.message_handler(AdminCheck(), commands=['get_all_teachers'])
async def get_all_teachers(message: types.Message):
    await create_teachers()
    await message.reply('Учителя сохранены в базе')


@dp.message_handler(AdminCheck(), commands=['save_photos'])
async def save_photos(message: types.Message):
    teachers_from_db = await teachers.select_all_teachers()



