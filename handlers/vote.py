import io
from logging import log, INFO

from aiogram import types
from aiogram.dispatcher.filters import Text, Regexp

from loader import dp, teachers, messages, users


@dp.message_handler(commands=['vote'])
@dp.message_handler(Text(equals='голосование', ignore_case=True))
async def make_vote(message: types.Message):
    vote = await teachers.select_parameter('vote')
    if vote == "0":
        await message.answer('Голосование сейчас не проводится')
    if vote == "1":
        teachers_in_group_1 = await teachers.select_teachers_by_finalist_group()
        keyboard_group_1 = types.InlineKeyboardMarkup()
        for teacher in teachers_in_group_1:
            keyboard_group_1.add(
                types.InlineKeyboardButton(
                    text=f"{teacher['full_name']}",
                    callback_data=f"select_teacher_before_vote={teacher['id']}",
                )
            )
        await message.answer('ВНИМАНИЕ! У вас будет одна попытка!')
        await message.answer("Выберите участника:", reply_markup=keyboard_group_1)
    # if vote == "2":
    #     teachers_in_group_2 = await teachers.select_teachers_by_finalist_group(group_id=2)
    #     keyboard_group_2 = types.InlineKeyboardMarkup()
    #     for teacher in teachers_in_group_2:
    #         keyboard_group_2.add(
    #             types.InlineKeyboardButton(
    #                 text=f"{teacher['full_name']}",
    #                 callback_data=f"select_teacher_before_vote=2={teacher['id']}",
    #             )
    #         )
    #     await message.answer("Выберите участника", reply_markup=keyboard_group_2)
    # if vote == "3":
    #     teachers_in_group_3 = await teachers.select_teachers_by_finalist_group(group_id=3)
    #     keyboard_group_3 = types.InlineKeyboardMarkup()
    #     for teacher in teachers_in_group_3:
    #         keyboard_group_3.add(
    #             types.InlineKeyboardButton(
    #                 text=f"{teacher['full_name']}",
    #                 callback_data=f"select_teacher_before_vote=3={teacher['id']}",
    #             )
    #         )
    #     await message.answer("Выберите участника", reply_markup=keyboard_group_3)


@dp.callback_query_handler(Regexp("select_teacher_before_vote=([0-9]*)"))
async def send_card_for_vote(callback: types.CallbackQuery):
    # group_id = int(callback.data.split('=')[1])
    teacher_id = int(callback.data.split('=')[1])
    teacher = await teachers.select_teacher(id=teacher_id)
    user = await users.select_user(telegram_id=callback.from_user.id)
    check = await teachers.check_vote(user['id'])
    await callback.message.delete()
    inline_keyboard = types.InlineKeyboardMarkup()
    if check:
        pass
    else:
        inline_keyboard.add(
            types.InlineKeyboardButton(
                text='Проголосовать',
                callback_data=f"vote_to={teacher_id}",
            )
        )
    inline_keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data=f"back_to_group",
        )
    )
    card_info = await messages.get_message('card_info')
    photo = teacher['photo_file_id'] if teacher['photo_file_id'] is not None else io.BytesIO(teacher['photo_raw_file'])
    await callback.message.answer_photo(
        photo=photo,
        caption=card_info.format(full_name=teacher['full_name'],
                                 region=teacher['region'],
                                 subject=', '.join(teacher['subject'])),
        reply_markup=inline_keyboard
    )


@dp.callback_query_handler(Regexp("back_to_group"))
async def back_to_group(callback: types.CallbackQuery):
    await callback.message.delete()
    # group_id = int(callback.data.split('=')[1])
    teachers_in_group = await teachers.select_teachers_by_finalist_group()
    keyboard_group = types.InlineKeyboardMarkup()
    for teacher in teachers_in_group:
        keyboard_group.add(
            types.InlineKeyboardButton(
                text=f"{teacher['full_name']}",
                callback_data=f"select_teacher_before_vote={teacher['id']}",
            )
        )
    await callback.message.answer("Выберите участника", reply_markup=keyboard_group)


@dp.callback_query_handler(Regexp("vote_to=([0-9]*)"))
async def make_vote(callback: types.CallbackQuery):
    # await callback.message.delete()
    vote = await teachers.select_parameter('vote')
    if vote == "0":
        await callback.message.answer('Голосование сейчас не проводится')
    elif vote == "1":
        user = await users.select_user(telegram_id=callback.from_user.id)
        teacher_id = int(callback.data.split('=')[1])
        await teachers.make_vote(user['id'], teacher_id)
        await teachers.update_ug2022_3_on()
        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.add(
            types.InlineKeyboardButton(
                text='Назад',
                callback_data=f"back_to_group",
            )
        )
        await callback.message.edit_reply_markup(inline_keyboard)

