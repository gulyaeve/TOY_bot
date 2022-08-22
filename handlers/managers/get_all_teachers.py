import io

from aiogram import types
from aiogram.dispatcher.filters import Text

from filters import ManagerCheck
from loader import dp, teachers, messages


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
    await callback.message.edit_text(await messages.get_message('choose_letter'), reply_markup=inline_keyboard)


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
    await message.answer(await messages.get_message('choose_letter'), reply_markup=inline_keyboard)


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
    await callback.message.delete()
    await callback.message.answer(await messages.get_message('choose_teacher'), reply_markup=inline_keyboard)


@dp.callback_query_handler(Text(startswith='teacher='))
async def get_teacher_info(callback: types.CallbackQuery):
    teacher_id = callback.data.split('=')[1]
    teacher = await teachers.select_teacher(id=int(teacher_id))
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(
        types.InlineKeyboardButton(
            text="◀️",
            callback_data=f"teacher_letter={teacher['full_name'][0]}"
        )
    )
    await callback.message.delete()
    card_info = await messages.get_message('card_info')
    photo = teacher['photo_file_id'] if teacher['photo_file_id'] is not None else io.BytesIO(teacher['photo_raw_file'])
    await callback.message.answer_photo(
        photo=photo,
        caption=card_info.format(full_name=teacher['full_name'],
                                 region=teacher['region'],
                                 subject=', '.join(teacher['subject'])),
        reply_markup=inline_keyboard
    )

