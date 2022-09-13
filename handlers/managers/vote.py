from aiogram import types
from aiogram.dispatcher.filters import Text

from filters import ManagerCheck
from loader import dp, teachers


@dp.message_handler(ManagerCheck(), commands=['vote'])
async def start_vote(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(
        types.InlineKeyboardButton(
            text='Группа 1',
            callback_data='vote_1'
        )
    )
    inline_keyboard.add(
        types.InlineKeyboardButton(
            text='Группа 2',
            callback_data='vote_2'
        )
    )
    inline_keyboard.add(
        types.InlineKeyboardButton(
            text='Группа 3',
            callback_data='vote_3'
        )
    )
    inline_keyboard.add(
        types.InlineKeyboardButton(
            text='Остановить голосование',
            callback_data='vote_0'
        )
    )
    await message.answer('Выберите группу для начала голосования:', reply_markup=inline_keyboard)


@dp.callback_query_handler(Text(equals='vote_1'))
async def vote_1(callback: types.CallbackQuery):
    await teachers.update_parameter('vote', '1')
    await callback.message.answer('Начато голосование группа 1')


@dp.callback_query_handler(Text(equals='vote_2'))
async def vote_1(callback: types.CallbackQuery):
    await teachers.update_parameter('vote', '2')
    await callback.message.answer('Начато голосование группа 2')


@dp.callback_query_handler(Text(equals='vote_3'))
async def vote_1(callback: types.CallbackQuery):
    await teachers.update_parameter('vote', '3')
    await callback.message.answer('Начато голосование группа 3')


@dp.callback_query_handler(Text(equals='vote_0'))
async def vote_1(callback: types.CallbackQuery):
    await teachers.update_parameter('vote', '0')
    await callback.message.answer('Остановлено голосование')
