from .base import BaseMiddleware


class HandlerMiddlewares:
    def __init__(self, func: callable, data: dict, args: list, update, middlewares: list[BaseMiddleware]):
        self.func = func
        self.args = args
        self.update = update
        self.middlewares = middlewares
        self.data = data
        self.number = 0

    async def __call__(self, data: dict = {}):
        self.number += 1
        self.data.update({key: value for key, value in data.items() if key in self.args})
        if self.number == len(self.middlewares):
            await self.func(self.update, **self.data)

    async def start(self):
        for middleware in self.middlewares:
            await middleware(handler=self, update=self.update, data={})