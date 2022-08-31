from aiogram import types

from loader import dp, teachers
from misc.split_to_groups import image_process


@dp.message_handler(commands=['split'])
async def split_to_groups(message: types.Message):
    all_teachers = await teachers.select_all_teachers()
    msg = ""
    for teacher in all_teachers:
        image = await teachers.get_photo(teacher['id'])
        result = image_process(image)
        msg += f"{result}\n"
    await message.answer(msg)
