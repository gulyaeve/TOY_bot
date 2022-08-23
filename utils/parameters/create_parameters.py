import json
from logging import log, INFO

from asyncpg import UniqueViolationError

from loader import teachers


async def create_parameters():
    with open("templates/parameters.json", "r", encoding="utf-8") as file:
        new_parameters = json.loads(file.read())
    for key, value in new_parameters.items():
        try:
            await teachers.add_parameter(key, value)
            log(INFO, "Parameter success saved to DB")
        except UniqueViolationError:
            log(INFO, "Parameter already in DB")


