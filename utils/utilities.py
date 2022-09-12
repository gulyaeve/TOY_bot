import io
import os
import re
from logging import log, INFO

from aiogram import types

from loader import bot, users


async def get_bot_info() -> types.User:
    me = await bot.get_me()
    return me


async def get_users_file() -> types.InputFile:
    filename = "users.txt"
    list_users = await users.select_all_users()
    answer = "{:4}. {:25} {:20} {:11}\n".format(
        "   №", "full_name", "username", "telegram_id"
    )
    for user in list_users:
        answer += "{:4}. {:25} {:20} {:11}\n".format(
            user['id'],
            user['full_name'],
            str(user['username']),
            user['telegram_id'],
        )
    return types.InputFile(io.BytesIO(make_bytes(answer, filename)), filename)


def make_keyboard_dict(buttons: dict):
    keyboard = types.ReplyKeyboardMarkup()
    for button in buttons.values():
        keyboard.add(button)
    keyboard.add("ОТМЕНА")
    return keyboard


def make_keyboard_list(buttons: list):
    keyboard = types.ReplyKeyboardMarkup()
    for button in buttons:
        keyboard.add(button)
    keyboard.add("ОТМЕНА")
    return keyboard


def make_text(input_text):
    return re.sub(r'<.*?>', '', input_text)


def make_bytes(file_content: str, file_label: str) -> bytes:
    with open(f"temp/{file_label}", "w") as f:
        f.write(file_content)
    with open(f"temp/{file_label}", "rb") as f:
        file = f.read()
        b = bytearray(file)
    os.remove(f"temp/{file_label}")
    return b


def make_dict_output(d: types.User) -> str:
    result = ''
    d = dict(d)
    for key, value in d.items():
        result += "{0}: {1}\n".format(key, value)
    return result
