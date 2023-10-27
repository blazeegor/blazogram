from .base import BaseMiddleware

class HandlerMiddlewares:
    def __init__(self, func: callable, data: dict, args: list, update, middlewares: list[BaseMiddleware]):
        self.func = func
        self.args = args
        self.update = update
        self.middlewares = middlewares
        self.data = data

    async def __call__(self):
        for key in self.data.keys():
            if key not in self.args:
                del self.data[key]

        await self.func(self.update, **self.data)

    async def start(self):
        for index, middleware in enumerate(self.middlewares):
            await middleware(handler=self, update=self.update, data=self.data)
