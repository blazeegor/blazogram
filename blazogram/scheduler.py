import asyncio
from datetime import datetime


async def run(func: callable, run_date: datetime, kwargs: dict):
    await asyncio.sleep((run_date - datetime.now()).total_seconds())
    await func(**kwargs)


class BlazeScheduler:
    def __init__(self):
        self.jobs = []

    def add_job(self, func: callable, run_date: datetime, kwargs: dict):
        self.jobs.append((func, run_date, kwargs,))

    async def remove_jobs(self):
        for job in self.jobs:
            self.jobs.remove(job)

    async def start(self):
        while True:
            await asyncio.sleep(1)
            if self.jobs:
                task_1 = asyncio.create_task(self.remove_jobs())
                task_2 = asyncio.create_task(self.start())
                await asyncio.wait([asyncio.create_task(run(func=job[0], run_date=job[1], kwargs=job[2])) for job in self.jobs])
                await task_1
                await task_2
                break