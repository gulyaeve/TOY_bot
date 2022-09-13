from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, teachers


@dp.message_handler(Text(equals='голосование'.lower()), commands=['vote'])
async def make_vote(message: types.Message):
    vote = await teachers.select_parameter('vote')
    if vote == 0:
        await message.answer('Голосование сейчас не проводится')


