from logging import log, INFO

from aiogram import types

from filters import ManagerCheck
from loader import dp, teachers


@dp.message_handler(ManagerCheck(), commands=['start_web'])
async def start_web(message: types.Message):
    json = await teachers.get_json_with_finalists()
    log(INFO, json)
    await teachers.update_ug2022(json)
    await message.answer(f"Смотри анимацию")

