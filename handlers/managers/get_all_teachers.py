import io

from aiogram import types
from aiogram.dispatcher.filters import Text, Regexp

from filters import ManagerCheck
from loader import dp, teachers, messages
from utils.db_api.teachers import MaxFinalistReached


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
    teacher_id = int(callback.data.split('=')[1])
    teacher = await teachers.select_teacher(id=teacher_id)
    count_finalists = await teachers.count_finalists()
    max_finalists = await teachers.select_parameter('max_finalists')
    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_finalist_on = types.InlineKeyboardButton(
            text=f"({count_finalists}/{max_finalists}) Сделать финалистом 🏁",
            callback_data=f"make_finalist={teacher['id']}"
        )
    button_finalist_off = types.InlineKeyboardButton(
            text=f"({count_finalists}/{max_finalists}) Убрать финалиста ❌",
            callback_data=f"delete_finalist={teacher['id']}"
        )
    check_finalist = await teachers.check_finalist(teacher['id'])
    button = button_finalist_on if check_finalist is not True else button_finalist_off
    inline_keyboard.add(
        button,
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


@dp.callback_query_handler(Regexp('make_finalist=([0-9]*)'))
async def save_finalist(callback: types.CallbackQuery):
    teacher_id = int(callback.data.split('=')[1])
    teacher = await teachers.select_teacher(id=teacher_id)
    max_finalists = await teachers.select_parameter('max_finalists')
    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    try:
        await teachers.save_finalist(id=teacher_id)
        count_finalists = await teachers.count_finalists()
        button_finalist_on = types.InlineKeyboardButton(
            text=f"({count_finalists}/{max_finalists}) Сделать финалистом 🏁",
            callback_data=f"make_finalist={teacher['id']}"
        )
        button_finalist_off = types.InlineKeyboardButton(
            text=f"({count_finalists}/{max_finalists}) Убрать финалиста ❌",
            callback_data=f"delete_finalist={teacher['id']}"
        )
        check_finalist = await teachers.check_finalist(teacher['id'])
        button = button_finalist_on if check_finalist is not True else button_finalist_off
    except MaxFinalistReached:
        button = types.InlineKeyboardButton(
            text=f"Уже {max_finalists} финалистов 🛑",
            callback_data=f"max_finalist_reached"
        )
    inline_keyboard.add(
        button,
        types.InlineKeyboardButton(
            text="◀️",
            callback_data=f"teacher_letter={teacher['full_name'][0]}"
        )
    )
    await callback.message.edit_reply_markup(inline_keyboard)


@dp.callback_query_handler(Regexp('delete_finalist=([0-9]*)'))
async def delete_finalist(callback: types.CallbackQuery):
    teacher_id = int(callback.data.split('=')[1])
    teacher = await teachers.select_teacher(id=teacher_id)
    max_finalists = await teachers.select_parameter('max_finalists')
    await teachers.delete_finalist(id=teacher_id)
    count_finalists = await teachers.count_finalists()
    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_finalist_on = types.InlineKeyboardButton(
        text=f"({count_finalists}/{max_finalists}) Сделать финалистом 🏁",
        callback_data=f"make_finalist={teacher['id']}"
    )
    button_finalist_off = types.InlineKeyboardButton(
        text=f"({count_finalists}/{max_finalists}) Убрать финалиста ❌",
        callback_data=f"delete_finalist={teacher['id']}"
    )
    check_finalist = await teachers.check_finalist(teacher['id'])
    button = button_finalist_on if check_finalist is not True else button_finalist_off
    inline_keyboard.add(
        button,
        types.InlineKeyboardButton(
            text="◀️",
            callback_data=f"teacher_letter={teacher['full_name'][0]}"
        )
    )
    await callback.message.edit_reply_markup(inline_keyboard)


@dp.callback_query_handler(Text("max_finalist_reached"))
async def max_finalists(callback: types.CallbackQuery):
    max_finalists = await teachers.select_parameter('max_finalists')
    await callback.answer(f'Уже {max_finalists} финалистов!')
