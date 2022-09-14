import asyncio
import json
from logging import log, INFO

import asyncpg

from utils.db_api.db import Database


class MaxFinalistReached(Exception):
    pass


class Teachers(Database):
    def __init__(self):
        super().__init__()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.create_tables())

    async def create_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS teachers (
            id int UNIQUE,
            full_name character varying(255),
            region character varying(255),
            subject text[],
            photo_file_id text,
            photo_raw_file bytea
        );
        CREATE TABLE IF NOT EXISTS finalists (
            id int UNIQUE NOT NULL references teachers(id),
            group_id int default 0
        );
        CREATE TABLE IF NOT EXISTS parameters (
            id serial NOT NULL UNIQUE,
            description text UNIQUE,
            value character varying(255)
        );
        CREATE TABLE IF NOT EXISTS poll_1 (
            id serial NOT NULL UNIQUE,
            user_id int NOT NULL UNIQUE,
            teacher_id int NOT NULL,
            time_created timestamp without time zone DEFAULT timezone('utc'::text, now())
        );
        CREATE TABLE IF NOT EXISTS poll_2 (
            id serial NOT NULL UNIQUE,
            user_id int NOT NULL UNIQUE,
            teacher_id int NOT NULL,
            time_created timestamp without time zone DEFAULT timezone('utc'::text, now())
        );
        CREATE TABLE IF NOT EXISTS poll_3 (
            id serial NOT NULL UNIQUE,
            user_id int NOT NULL UNIQUE,
            teacher_id int NOT NULL,
            time_created timestamp without time zone DEFAULT timezone('utc'::text, now())
        );
        """
        await self.execute(sql, execute=True)

    # Пользователи
    async def add_teacher(self, id: int, full_name: str, region: str, subject: list, file_id, raw_file) -> asyncpg.Record:
        sql = "INSERT INTO teachers (id, full_name, region, subject, photo_file_id, photo_raw_file)" \
              "VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, id, full_name, region, subject, file_id, raw_file, fetchrow=True)

    async def update_teacher_photo_id(self, file_id: str, id: int) -> asyncpg.Record:
        sql = "UPDATE teachers SET photo_file_id=$1 WHERE id=$2"
        return await self.execute(sql, file_id, id, execute=True)

    async def update_finalist_group(self, finalist_id: int, group_id: int):
        sql = "UPDATE finalists SET group_id=$2 WHERE id=$1"
        return await self.execute(sql, finalist_id, group_id, execute=True)

    async def select_all_teachers(self) -> list[asyncpg.Record]:
        sql = "SELECT * FROM teachers ORDER BY full_name ASC"
        return await self.execute(sql, fetch=True)

    async def select_all_finalists(self) -> list[asyncpg.Record]:
        sql = "SELECT * FROM finalists ORDER BY group_id ASC"
        return await self.execute(sql, fetch=True)

    async def select_teacher(self, **kwargs) -> asyncpg.Record:
        sql = "SELECT * FROM teachers WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def save_finalist(self, id: str) -> asyncpg.Record:
        count_finalists = await self.count_finalists()
        max_finalists = await self.select_parameter('max_finalists')
        if count_finalists < int(max_finalists):
            sql = "INSERT INTO finalists (id) VALUES($1) returning *"
            return await self.execute(sql, id, fetchrow=True)
        else:
            raise MaxFinalistReached

    async def select_finalist(self, **kwargs) -> asyncpg.Record:
        sql = "SELECT * FROM finalists WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_teachers_by_finalist_group(self, group_id: int) -> list[asyncpg.Record]:
        sql = "SELECT id FROM finalists WHERE group_id=$1"
        teachers = await self.execute(sql, group_id, fetch=True)
        results = []
        for record in teachers:
            teacher = await self.select_teacher(id=record['id'])
            results.append(teacher)
        return results

    async def vote_poll_1(self, user_id: int, teacher_id: int):
        sql = "INSERT INTO poll_1 (user_id, teacher_id) VALUES($1, $2)"
        return await self.execute(sql, user_id, teacher_id, execute=True)

    async def vote_poll_2(self, user_id: int, teacher_id: int):
        sql = "INSERT INTO poll_2 (user_id, teacher_id) VALUES($1, $2)"
        return await self.execute(sql, user_id, teacher_id, execute=True)

    async def vote_poll_3(self, user_id: int, teacher_id: int):
        sql = "INSERT INTO poll_3 (user_id, teacher_id) VALUES($1, $2)"
        return await self.execute(sql, user_id, teacher_id, execute=True)

    async def count_finalists(self):
        sql = "SELECT COUNT(*) FROM finalists"
        return await self.execute(sql, fetchval=True)

    async def clear_finalists(self):
        sql = "TRUNCATE TABLE finalists"
        await self.execute(sql, execute=True)

    async def check_finalist(self, id: int) -> bool:
        finalist = await self.select_finalist(id=id)
        return True if finalist is not None else False

    async def delete_finalist(self, id: int):
        await self.execute("DELETE FROM finalists WHERE id=$1", id, execute=True)

    async def add_parameter(self, description: str, value: str) -> asyncpg.Record:
        sql = "INSERT INTO parameters (description, value) VALUES($1, $2) returning *"
        return await self.execute(sql, description, value, fetchrow=True)

    async def select_parameter(self, description: str) -> str:
        sql = "SELECT value FROM parameters WHERE description=$1"
        return await self.execute(sql, description, fetchval=True)

    async def update_parameter(self, description: str, new_value: str):
        sql = "UPDATE parameters SET value=$2 WHERE description=$1"
        return await self.execute(sql, description, new_value, execute=True)

    async def get_photo(self, id: int) -> bytes:
        sql = "SELECT photo_raw_file FROM teachers WHERE id=$1"
        return await self.execute(sql, id, fetchval=True)

    async def update_ug2022(self, json: str):
        sql = "UPDATE ug2022 SET data=$1 WHERE id=2"
        sql2 = "UPDATE ug2022 SET status=1 WHERE id=1"
        await self.execute(sql, json, execute=True)
        await self.execute(sql2, execute=True)

    async def get_json_with_finalists(self) -> dict:
        sql = "SELECT teachers.full_name AS name, CONCAT('assets/img/photo/', teachers.full_name, '.png') AS photo, finalists.group_id FROM teachers JOIN finalists ON teachers.id = finalists.id ORDER BY teachers.full_name"
        records = await self.execute(sql, fetch=True)
        json_1 = {"part": []}
        for record in records:
            log(INFO, record)
            json_1['part'].append({"name": record['name'], "photo": record['photo'], "group": record['group_id']})
        return json.loads(str(json_1))
    #
    # async def delete_users(self):
    #     await self.execute("DELETE FROM users WHERE TRUE", execute=True)
    #
    # async def drop_users(self):
    #     await self.execute("DROP TABLE IF EXISTS users", execute=True)
    #
    # # Типы пользователей
    # async def add_user_type(self, name: str) -> asyncpg.Record:
    #     sql = "INSERT INTO type_users_list (name) VALUES($1) returning *"
    #     return await self.execute(sql, name, fetchrow=True)
    #
    # async def select_user_type(self, user_type: str) -> asyncpg.Record:
    #     sql = "SELECT * FROM type_users_list WHERE name=$1"
    #     return await self.execute(sql, user_type, fetchrow=True)
    #
    # async def select_users_by_type(self, type_user_id: int) -> list:
    #     sql = "SELECT * FROM users WHERE type_user_id=$1"
    #     return await self.execute(sql, type_user_id, fetch=True)
    #
    # async def update_user_type(self, new_type: int, id: int) -> asyncpg.Record:
    #     sql = "UPDATE users SET type_user_id=$1 WHERE id=$2"
    #     return await self.execute(sql, new_type, id, execute=True)
