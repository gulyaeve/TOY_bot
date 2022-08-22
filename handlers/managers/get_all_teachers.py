import io

from aiogram import types
from aiogram.dispatcher.filters import Text

from filters import ManagerCheck
from loader import dp, teachers
from utils.teachers.create_teachers import create_teachers


@dp.message_handler(ManagerCheck(), commands=['get_all_teachers'])
async def get_all_teachers(message: types.Message):
    await create_teachers()
    await message.reply('Учителя сохранены в базе')


@dp.callback_query_handler(text='back_to_letters')
async def create_finalists(callback: types.CallbackQuery):
    teachers_from_db = await teachers.select_all_teachers()
    inline_keyboard = types.InlineKeyboardMarkup(row_width=7)
    letters = set()
    for teacher in teachers_from_db:
        letters.add(teacher['full_name'][0])
    letters_list = sorted(list(letters))
    for letter in letters_list:
        inline_keyboard.insert(
            types.InlineKeyboardButton(
                text=letter, callback_data=f'teacher_letter={letter}'
            )
        )
    await callback.message.edit_text('Выберите первую букву фамилии:', reply_markup=inline_keyboard)


@dp.message_handler(ManagerCheck(), commands=['create_finalists'])
async def create_finalists(message: types.Message):
    teachers_from_db = await teachers.select_all_teachers()
    inline_keyboard = types.InlineKeyboardMarkup(row_width=7)
    letters = set()
    for teacher in teachers_from_db:
        letters.add(teacher['full_name'][0])
    letters_list = sorted(list(letters))
    for letter in letters_list:
        inline_keyboard.insert(
            types.InlineKeyboardButton(
                text=letter, callback_data=f'teacher_letter={letter}'
            )
            )
    await message.answer('Выберите первую букву фамилии:', reply_markup=inline_keyboard)


@dp.callback_query_handler(Text(startswith='teacher_letter='))
async def get_finalists_for_letter(callback: types.CallbackQuery):
    letter = callback.data.split('=')[1]
    teachers_from_db = await teachers.select_all_teachers()
    inline_keyboard = types.InlineKeyboardMarkup()
    for teacher in teachers_from_db:
        if teacher['full_name'][0] == letter:
            inline_keyboard.add(
                types.InlineKeyboardButton(
                    text=teacher['full_name'],
                    callback_data=f"teacher={teacher['id']}"
                )
            )
    inline_keyboard.add(
        types.InlineKeyboardButton(
            text="◀️",
            callback_data='back_to_letters'
        )
    )
    await callback.message.edit_text('Выберите участника:', reply_markup=inline_keyboard)


@dp.callback_query_handler(Text(startswith='teacher='))
async def get_teacher_info(callback: types.CallbackQuery):
    teacher_id = callback.data.split('=')[1]
    teacher = await teachers.select_teacher(id=int(teacher_id))
    await callback.message.answer_photo(
        photo=io.BytesIO(teacher['photo_raw_file']),
        caption=f"ФИО: <i>{teacher['full_name']}</i>\n"
                f"Регион: <i>{teacher['region']}</i>\n"
                f"Предмет: <i>{' '.join(teacher['subject'])}</i>\n"
    )

