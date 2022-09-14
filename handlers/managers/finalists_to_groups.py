import asyncio
from io import BytesIO

from aiogram import types

from filters import ManagerCheck
from loader import dp, teachers, messages
import random
import numpy


@dp.message_handler(ManagerCheck(), commands=['finalists'])
async def show_finalists(message: types.Message):
    all_finalists = await teachers.select_all_finalists()
    max_finalists = await teachers.select_parameter('max_finalists')
    if all_finalists.__len__() == int(max_finalists):
        for finalist in all_finalists:
            teacher = await teachers.select_teacher(id=finalist['id'])
            card_info = await messages.get_message('card_info')
            photo = teacher['photo_file_id'] if teacher['photo_file_id'] is not None else BytesIO(teacher['photo_raw_file'])
            await message.answer_photo(
                photo=photo,
                caption=card_info.format(full_name=teacher['full_name'],
                                         region=teacher['region'],
                                         subject=', '.join(teacher['subject']))
            )
            await asyncio.sleep(0.3)
    else:
        answer = await messages.get_message("not_finalists")
        await message.answer(answer.format(all_finalists.__len__(), max_finalists))


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
        await message.answer("Финалисты поделены на группы, для просмотра групп: <b>/groups</b>")
    else:
        answer = await messages.get_message("not_finalists")
        await message.answer(answer.format(all_finalists.__len__(), max_finalists))


@dp.message_handler(ManagerCheck(), commands=['groups'])
async def send_group_list(message: types.Message):
    all_finalists = await teachers.select_all_finalists()
    max_finalists = await teachers.select_parameter('max_finalists')
    if all_finalists.__len__() == int(max_finalists):
        msg = ""
        group_0 = ""
        group_1 = ""
        group_2 = ""
        group_3 = ""
        for finalist in all_finalists:
            finalist_data = await teachers.select_teacher(id=finalist['id'])
            finalist_info = f"{finalist_data['full_name']}"
            if finalist['group_id'] == 1:
                group_1 += f"{finalist_info}\n"
            if finalist['group_id'] == 2:
                group_2 += f"{finalist_info}\n"
            if finalist['group_id'] == 3:
                group_3 += f"{finalist_info}\n"
            # else:
            #     group_0 += f"{finalist_info}\n"
        if group_0 == "":
            msg = f"<b>Группа 1:</b>\n{group_1}\n" \
                  f"<b>Группа 2:</b>\n{group_2}\n" \
                  f"<b>Группа 3:</b>\n{group_3}\n"
        else:
            msg = f"<b>Без группы:</b>\n{group_0}"
        await message.answer(msg)
    else:
        answer = await messages.get_message("not_finalists")
        await message.answer(answer.format(all_finalists.__len__(), max_finalists))
