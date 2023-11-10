import asyncio
from datetime import datetime, timedelta
from .storage.base import Job


class BlazeScheduler:
    def __init__(self):
        self.jobs: list[Job] = []

    def add_job(self, func: callable, run_date: datetime = datetime.now(), number_repetitions: int = 1, interval_time: timedelta = timedelta(seconds=0.5), is_forever: bool = False, kwargs: dict = dict):
        self.jobs.append(Job(func=func, run_date=run_date,
                             number_repetitions=number_repetitions, interval_time=interval_time,
                             is_forever=is_forever, kwargs=kwargs))

    async def start(self, dispatcher):
        while dispatcher.keep_polling is True:
            await asyncio.sleep(1)
            if self.jobs:
                await asyncio.wait([asyncio.create_task(self._run(job=job)) for job in self.jobs.copy()])
                task_1 = asyncio.create_task(self.start(dispatcher=dispatcher))
                await task_1
                self.jobs.clear()
                break

    @staticmethod
    async def _run(job: Job):
        await asyncio.sleep((job.run_date - datetime.now()).total_seconds())
        number = 0
        while number < job.number_repetitions if job.is_forever is False else True:
            await job.func(**job.kwargs)
            await asyncio.sleep(job.interval_time.total_seconds())
            number += 1