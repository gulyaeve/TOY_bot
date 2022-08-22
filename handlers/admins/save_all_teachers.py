import io
from logging import log, INFO

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
    for teacher in teachers_from_db:
        if teacher['photo_file_id'] is None:
            new_message = await message.answer_photo(types.InputFile(io.BytesIO(teacher['photo_raw_file'])))
            await teachers.update_teacher_photo_id(new_message.photo[-1].file_id, teacher['id'])
            log(INFO, f"Photo_id saved for [{teacher['id']}]")




