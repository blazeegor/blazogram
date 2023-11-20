import asyncio


class InputFile:
    def __init__(self, filename: str):
        self.file = open(filename, "rb")
        asyncio.create_task(self.close_file())

    async def close_file(self):
        await asyncio.sleep(5)
        self.file.close()
