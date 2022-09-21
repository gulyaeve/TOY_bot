import asyncio
from logging import log, INFO

from aiogram import types
from aiogram.dispatcher.filters import Text

from filters import ManagerCheck
from loader import dp, teachers, users


@dp.message_handler(ManagerCheck(), commands=['start_vote'])
async def start_vote(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(
        types.InlineKeyboardButton(
            text='Начать голосование',
            callback_data='vote_1'
        )
    )
    # inline_keyboard.add(
    #     types.InlineKeyboardButton(
    #         text='Группа 2',
    #         callback_data='vote_2'
    #     )
    # )
    # inline_keyboard.add(
    #     types.InlineKeyboardButton(
    #         text='Группа 3',
    #         callback_data='vote_3'
    #     )
    # )
    inline_keyboard.add(
        types.InlineKeyboardButton(
            text='Остановить голосование',
            callback_data='vote_0'
        )
    )
    await message.answer('Выберите действие:', reply_markup=inline_keyboard)


@dp.callback_query_handler(Text(equals='vote_1'))
async def vote_1(callback: types.CallbackQuery):
    await teachers.update_parameter('vote', '1')
    await teachers.update_ug2022_3_start()
    await callback.message.answer('Голосование началось')
    users_to_send: list = await users.select_all_users()
    for user in users_to_send:
        await asyncio.sleep(0.1)
        try:
            await dp.bot.send_message(user['telegram_id'], '⚡️⚡️⚡️\nГолосование началось <b>/vote</b>')
            log(INFO, f"ГОЛОСОВАНИЕ Рассылка успешно отправлена пользователю {user['telegram_id']}")
        except:
            log(INFO, f"ГОЛОСОВАНИЕ Ошибка при отправке рассылки пользователю {user['telegram_id']}")


# @dp.callback_query_handler(Text(equals='vote_2'))
# async def vote_1(callback: types.CallbackQuery):
#     await teachers.update_parameter('vote', '2')
#     await callback.message.answer('Начато голосование группа 2')
#
#
# @dp.callback_query_handler(Text(equals='vote_3'))
# async def vote_1(callback: types.CallbackQuery):
#     await teachers.update_parameter('vote', '3')
#     await callback.message.answer('Начато голосование группа 3')


@dp.callback_query_handler(Text(equals='vote_0'))
async def vote_1(callback: types.CallbackQuery):
    await teachers.update_parameter('vote', '0')
    await teachers.update_ug2022_3_stop()
    await callback.message.answer('Остановлено голосование')
    users_to_send: list = await users.select_all_users()
    for user in users_to_send:
        await asyncio.sleep(0.1)
        try:
            await dp.bot.send_message(user['telegram_id'], "Голосование завершено!")
            log(INFO, f"ГОЛОСОВАНИЕ Рассылка успешно отправлена пользователю {user['telegram_id']}")
        except:
            log(INFO, f"ГОЛОСОВАНИЕ Ошибка при отправке рассылки пользователю {user['telegram_id']}")


@dp.message_handler(ManagerCheck(), commands=['count_votes'])
async def count_votes(message: types.Message):
    votes = await teachers.count_votes()
    await message.answer(f"Количество голосов: {votes}")
