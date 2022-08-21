from aiogram import types
from keyboards.admin import AdminCallbacks
from loader import dp
from utils.utilities import get_users_file


@dp.callback_query_handler(text=AdminCallbacks.get_users.value)
async def get_users(callback: types.CallbackQuery):
    users_file = await get_users_file()
    await callback.answer("Выгружаю")
    await callback.message.edit_text("Готово:", reply_markup=None)
    await callback.message.answer_document(users_file, caption="Список пользователей")

