import asyncio

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
            id int UNIQUE references teachers(id),
            group_id int default 0
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

    async def select_all_teachers(self) -> list:
        sql = "SELECT * FROM teachers"
        return await self.execute(sql, fetch=True)

    async def select_teacher(self, **kwargs) -> asyncpg.Record:
        sql = "SELECT * FROM teachers WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def save_finalist(self, id: str) -> asyncpg.Record:
        count_finalists = await self.count_finalists()
        if count_finalists < 15:
            sql = "INSERT INTO finalists (id) VALUES($1) returning *"
            return await self.execute(sql, id, fetchrow=True)
        else:
            raise MaxFinalistReached

    async def count_finalists(self):
        sql = "SELECT COUNT(*) FROM finalists"
        return await self.execute(sql, fetchval=True)

    # async def delete_user(self, telegram_id):
    #     await self.execute("DELETE FROM users WHERE telegram_id=$1", telegram_id, execute=True)
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
