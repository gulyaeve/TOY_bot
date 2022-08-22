from logging import log, INFO

from asyncpg import UniqueViolationError

from loader import users, teachers
from misc.parse_toy_site import get_teachers_list


async def create_teachers():
    # with open("templates/type_users_template.json", "r", encoding="utf-8") as file:
    #     new_types = json.loads(file.read())
    teachers_list = get_teachers_list()
    for teacher in teachers_list:
        try:
            new_teacher = await teachers.add_teacher(
                id=teacher['id'],
                full_name=teacher['full_name'],
                region=teacher['region'],
                subject=teacher['subject'],
                file_id=None,
                raw_file=teacher['photo_raw_file']
            )
            log(INFO, f"Teacher saved {new_teacher}")
        except UniqueViolationError:
            # exist_user_type = await users.select_user_type(user_type)
            log(INFO, f"Teacher exists {teacher}")
    log(INFO, "User types success saved to DB")
