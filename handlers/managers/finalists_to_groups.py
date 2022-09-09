from aiogram import types

from filters import ManagerCheck
from loader import dp, teachers
from misc.split_to_groups import image_process


@dp.message_handler(ManagerCheck(), commands=['split'])
async def split_to_groups(message: types.Message):
    all_finalists = await teachers.select_all_finalists()
    results = []
    for finalist in all_finalists:
        image = await teachers.get_photo(finalist['id'])
        result = image_process(image)
        results.append((finalist['id'], result))
    await message.answer(f"{results}")
