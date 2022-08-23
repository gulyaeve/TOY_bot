from logging import log, INFO

from asyncpg import UniqueViolationError

from loader import teachers
from misc.parse_toy_site import get_teachers_list


async def create_teachers():
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
            log(INFO, f"Teacher saved {new_teacher['id']}")
        except UniqueViolationError:
            log(INFO, f"Teacher exists {teacher}")
    log(INFO, "User types success saved to DB")
