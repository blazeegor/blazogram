from .base import Database
from ..types.user import User
from ..exceptions import DatabaseError
from pathlib import Path
from typing import Union
import aiosqlite
from aiosqlite import Cursor, Connection
import asyncio


class SQLite3(Database):
    def __init__(self, connection: Connection):
        self.connection = connection
        asyncio.create_task(self.start())

    async def start(self):
        query = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, first_name TEXT NOT NULL, last_name TEXT NOT NULL, username TEXT NOT NULL, is_bot TEXT NOT NULL)'
        await self.request(query=query)

    async def request(self, query: str, params: tuple = None):
        await self.connection.execute(query, params)
        await self.connection.commit()

    async def select(self, table: str, columns: list[str] | str, params: dict = None, fetch_all: bool = False, fetch_number: int = 1):
        cursor: Cursor = await self.connection.cursor()

        if isinstance(columns, list):
            take_columns = ''
            for column in columns:
                take_columns += column + ', '
            columns = take_columns[: -2]

        params_query = 'WHERE ' if params else None
        if params:
            for key, value in params.items():
                params_query += key + ' = ' + value + ' '

        result = await cursor.execute(f'SELECT {columns} FROM {table} {params_query}')
        result = await result.fetchmany(fetch_number)  if fetch_all is False else await result.fetchall()
        return result

    async def user_exist(self, user: User) -> bool:
        users = await self.get_users()
        return user in users

    async def add_user(self, user: User):
        if not await self.user_exist(user=user):
            try:
                await self.request(query='INSERT INTO users (user_id, first_name, last_name, username, is_bot) VALUES (?, ?, ?, ?, ?)', params=(user.id, user.first_name, user.last_name.__str__(), user.username, user.is_bot.__str__()))
            except Exception as ex:
                raise DatabaseError(message=ex.__str__())

    async def get_users(self) -> list[User]:
        cursor: Cursor = await self.connection.cursor()
        result = await cursor.execute('SELECT user_id, first_name, last_name, username, is_bot FROM users')
        users_res = await result.fetchall()
        users = [User(id=user[0], first_name=user[1], last_name=user[2] if user[2] != 'None' else None, username=user[3], is_bot=True if user[4] == 'True' else False) for user in users_res]
        return users

    async def close(self):
        await self.connection.close()