from logging import log, INFO

from aiogram import types

from filters import ManagerCheck
from loader import dp, teachers, messages


@dp.message_handler(ManagerCheck(), commands=['start_web'])
async def start_web(message: types.Message):
    all_finalists = await teachers.select_all_finalists()
    max_finalists = await teachers.select_parameter('max_finalists')
    if all_finalists.__len__() == int(max_finalists):
        json = await teachers.get_json_with_finalists()
        log(INFO, json)
        await teachers.update_ug2022(json)
        await message.answer(f"Смотри анимацию")
    else:
        answer = await messages.get_message("not_finalists")
        await message.answer(answer.format(all_finalists.__len__(), max_finalists))


@dp.message_handler(ManagerCheck(), commands=['stop_web'])
async def stop_web(message: types.Message):
    await teachers.update_ug2022_stop()
    await message.answer(f"Анимация остановлена")
