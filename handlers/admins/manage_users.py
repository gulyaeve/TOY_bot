from logging import log, INFO

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp, Text

from keyboards.admin import AdminCallbacks
from keyboards.keyboards import yes_no
from loader import dp, bot, users
from utils.utilities import get_users_file


@dp.callback_query_handler(text="back_to_manage_users_menu")
@dp.callback_query_handler(text=AdminCallbacks.manage_users.value)
async def choose_action(callback: types.CallbackQuery, state: FSMContext):
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(
        types.InlineKeyboardButton(text="Назначить менеджера",
                                   callback_data="set_manager")
    )
    inline_keyboard.add(types.InlineKeyboardButton(text="◀️", callback_data="back_to_main_admin_menu"))
    await callback.message.edit_text("Выберите действие:", reply_markup=inline_keyboard)


@dp.callback_query_handler(text="set_manager")
async def choose_manager(callback: types.CallbackQuery, state: FSMContext):
    users_file = await get_users_file()
    await callback.answer("Выгружаю")
    await callback.message.answer_document(users_file, caption="Список пользователей")
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(types.InlineKeyboardButton(text="◀️", callback_data="back_to_manage_users_menu"))
    await callback.message.edit_text("Введите id пользователя из базы:", reply_markup=inline_keyboard)
    await state.set_state("set_manager_by_id")


@dp.message_handler(Regexp('([0-9]*)'), state="set_manager_by_id")
async def enter_id(message: types.Message, state: FSMContext):
    id_to_set = int(message.text)
    async with state.proxy() as data:
        data['id_to_set'] = id_to_set
    user_to_set = await users.select_user(id=id_to_set)
    user_info = f"{user_to_set['full_name']}, @{user_to_set['username']}"
    await message.reply(f"Назначить менеджером <b>{user_info}?</b>", reply_markup=yes_no)
    await state.set_state("set_manager_confirm")


@dp.message_handler(Text(equals="Да"), state="set_manager_confirm")
async def set_manager(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_to_set = await users.select_user(id=data['id_to_set'])
    user_info = f"{user_to_set['full_name']}, @{user_to_set['username']}"
    manager_user_type = await users.select_user_type("manager")
    await users.update_user_type(manager_user_type['id'], user_to_set['id'])
    log(INFO, f"{message.from_user.id} set new manager {user_info}")
    await message.reply(f'Менеджер установлен <b>{user_info}</b>',
                        reply_markup=types.ReplyKeyboardRemove())
    try:
        await bot.send_message(user_to_set['telegram_id'], "Вы были назначены менеджером данного бота")
    except Exception as e:
        log(INFO, f"Failed to send to [{user_to_set['telegram_id']}] {e}")
    await state.finish()


@dp.message_handler(Text(equals="Нет"), state="set_manager_confirm")
async def dont_set_manager(message: types.Message, state: FSMContext):
    await message.reply('Назначение отменено.')
    await state.finish()
