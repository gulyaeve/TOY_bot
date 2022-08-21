import asyncio

import asyncpg

from utils.db_api.db import Database


class Users(Database):
    def __init__(self):
        super().__init__()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.create_tables())

    async def create_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS type_users_list (
            id SERIAL PRIMARY KEY,
            name text UNIQUE 
        );

        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            full_name character varying(255) NOT NULL,
            username character varying(255),
            telegram_id bigint NOT NULL UNIQUE,
            time_created timestamp without time zone DEFAULT timezone('utc'::text, now()),
            type_user_id integer REFERENCES type_users_list(id) DEFAULT 1
        );
        """
        await self.execute(sql, execute=True)

    # Пользователи
    async def add_user(self, full_name: str, username: str, telegram_id: int) -> asyncpg.Record:
        """
        Добавление пользователя в базу данных

        :param full_name: user's fullname from telegram
        :param username: user's username from telegram
        :param telegram_id: user's id from telegram
        :return:
        """
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def update_user_fullname(self, full_name: str, telegram_id: int) -> asyncpg.Record:
        sql = "UPDATE users SET full_name=$1 WHERE telegram_id=$2"
        return await self.execute(sql, full_name, telegram_id, execute=True)

    async def update_user_username(self, username: str, telegram_id: int) -> asyncpg.Record:
        sql = "UPDATE users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def select_all_users(self) -> list:
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs) -> asyncpg.Record:
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.execute(sql, fetchval=True)

    async def delete_user(self, telegram_id):
        await self.execute("DELETE FROM users WHERE telegram_id=$1", telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE IF EXISTS users", execute=True)

    # Типы пользователей
    async def add_user_type(self, name: str) -> asyncpg.Record:
        sql = "INSERT INTO type_users_list (name) VALUES($1) returning *"
        return await self.execute(sql, name, fetchrow=True)

    async def select_user_type(self, user_type: str) -> asyncpg.Record:
        sql = "SELECT * FROM type_users_list WHERE name=$1"
        return await self.execute(sql, user_type, fetchrow=True)

    async def select_users_by_type(self, type_user_id: int) -> list:
        sql = "SELECT * FROM users WHERE type_user_id=$1"
        return await self.execute(sql, type_user_id, fetch=True)

    async def update_user_type(self, new_type: int, id: int) -> asyncpg.Record:
        sql = "UPDATE users SET type_user_id=$1 WHERE id=$2"
        return await self.execute(sql, new_type, id, execute=True)
