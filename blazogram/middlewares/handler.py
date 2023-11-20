from .base import BaseMiddleware


class HandlerMiddlewares:
    def __init__(
        self,
        func: callable,
        data: dict,
        args: list,
        update,
        middlewares: list[BaseMiddleware],
    ):
        self.func = func
        self.args = args
        self.update = update
        self.middlewares = middlewares
        self.data = data
        self.number = 0

    async def __call__(self):
        self.number += 1
        if self.number == len(self.middlewares):
            for key in [key for key in self.data.keys()]:
                if key not in self.args:
                    self.data.pop(key)
            await self.func(self.update, **self.data)

    async def start(self):
        for middleware in self.middlewares:
            await middleware(handler=self, update=self.update, data=self.data)
