from aiogram import types

from filters import ManagerCheck
from loader import dp
from misc.parse_toy_site import get_teachers_list


@dp.message_handler(ManagerCheck(), commands=['get_all_teachers'])
async def get_all_teachers(message: types.Message):
    teachers_list = await get_teachers_list()
    for teacher in teachers_list:
        await message.answer_photo(types.InputFile(teacher['photo']),
                                   f"id: <code>{teacher['id']}</code>\n"
                                   f"Регион: <i>{teacher['region']}</i>\n"
                                   f"ФИО: <i>{teacher['full_name']}</i>")
