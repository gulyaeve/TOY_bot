import json
from logging import log, INFO

from asyncpg import UniqueViolationError

from loader import users


async def create_user_types():
    with open("templates/type_users_template.json", "r", encoding="utf-8") as file:
        new_types = json.loads(file.read())
    for user_type in new_types["type_users"]:
        try:
            new_user_type = await users.add_user_type(user_type)
            log(INFO, f"User type saved {new_user_type}")
        except UniqueViolationError:
            exist_user_type = await users.select_user_type(user_type)
            log(INFO, f"User type exist {exist_user_type}")
    log(INFO, "User types success saved to DB")
