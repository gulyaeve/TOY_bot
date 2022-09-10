from aiogram import types

from filters import ManagerCheck
from loader import dp, teachers
import random
import numpy


@dp.message_handler(ManagerCheck(), commands=['split'])
async def split_to_groups(message: types.Message):
    all_finalists = await teachers.select_all_finalists()
    max_finalists = await teachers.select_parameter('max_finalists')
    if all_finalists.__len__() == int(max_finalists):
        ids = []
        for finalist in all_finalists:
            ids.append(finalist['id'])
        random.shuffle(ids)
        splits = numpy.array_split(ids, 3)
        for idx, array in enumerate(splits):
            group_id = idx + 1
            for finalist in list(array):
                await teachers.update_finalist_group(finalist, group_id)
        await message.answer("Финалисты поделены на группы, для просмотра групп: /groups")
    else:
        await message.answer(f"Ещё не выбрано нужное число финалистов ({all_finalists.__len__()}/{max_finalists})")


@dp.message_handler(ManagerCheck(), commands=['groups'])
async def send_group_list(message: types.Message):
    all_finalists = await teachers.select_all_finalists()
    max_finalists = await teachers.select_parameter('max_finalists')
    if all_finalists.__len__() == int(max_finalists):
        msg = ""
        for finalist in all_finalists:
            msg += f"{finalist['group_id']}: {finalist['id']}\n"
        await message.answer(msg)
    else:
        await message.answer(f"Ещё не выбрано нужное число финалистов ({all_finalists.__len__()}/{max_finalists})")
