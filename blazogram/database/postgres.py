from .base import Database
import asyncpg
import asyncio
from asyncpg import Connection
from ..types.user import User
from ..exceptions import DatabaseError


class PostgreSQL(Database):
    def __init__(self, host: str, user: str, password: str, database: str, port: str = '5432'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        asyncio.create_task(self.start())

    async def start(self):
        connection: Connection = await asyncpg.connect(host=self.host, user=self.user, password=self.password, port=self.port)
        self.connection = connection
        await self.request('CREATE TABLE IF NOT EXISTS users (id bigint NOT NULL GENERATED ALWAYS AS IDENTITY (INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1), user_id bigint, first_name text, last_name text, username text, is_bot text)')

    async def request(self, query: str, params: tuple = None):
        try:
            await self.connection.execute(query, *params)
        except Exception as ex:
            raise DatabaseError(message=ex.__str__())

    async def select(self, table: str, columns: list[str] | str, params: dict = None, fetch_all: bool = False, fetch_number: int = 1):
        async with self.connection.transaction():
            if isinstance(columns, list):
                take_columns = ''
                for column in columns:
                    take_columns += column + ', '
                columns = take_columns[: -2]

            params_query = 'WHERE ' if params else None
            if params:
                for key, value in params.items():
                    params_query += key + ' = ' + value + ' '

            query = f'SELECT {columns} FROM {table} {params_query}'
            result = await self.connection.fetch(query) if fetch_all else await self.connection.cursor(query)
            if fetch_all is False:
                result = await result.fetch(fetch_number)

            return result

    async def user_exist(self, user: User) -> bool:
        users = await self.get_users()
        return user in users

    async def add_user(self, user: User):
        if not await self.user_exist(user=user):
            await self.request(query='INSERT INTO users (user_id, first_name, last_name, username, is_bot) VALUES ($1, $2, $3, $4, $5)', params=(user.id, user.first_name, user.last_name.__str__(), user.username, user.is_bot.__str__()))

    async def get_users(self) -> list[User]:
        result = await self.connection.fetch('SELECT user_id, first_name, last_name, username, is_bot FROM users')
        users = [User(id=user.get('user_id'), first_name=user.get('first_name'), last_name=user.get('last_name') if user.get('last_name') != 'None' else None, username=user.get('username'), is_bot=True if user.get('is_bot') == 'True' else False) for user in result]
        return users

    async def close(self):
        await self.connection.close()