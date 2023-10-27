import asyncio
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class Job:
    func: callable
    run_date: datetime
    number_repetitions: int
    interval_time: timedelta
    is_forever: bool
    kwargs: dict

class BlazeScheduler:
    def __init__(self):
        self.jobs: list[Job] = []

    def add_job(self, func: callable, run_date: datetime = datetime.now(), number_repetitions: int = 1, interval_time: timedelta = timedelta(seconds=0.5), is_forever: bool = False, kwargs: dict = dict):
        self.jobs.append(
            Job(func=func, run_date=run_date,
                number_repetitions=number_repetitions,
                interval_time=interval_time, is_forever=is_forever,
                kwargs=kwargs)
        )

    async def remove_jobs(self):
        self.jobs.clear()

    async def start(self):
        while self.jobs:
            for job in self.jobs.copy():
                await asyncio.sleep((job.run_date - datetime.now()).total_seconds())
                number = 0
                while number < job.number_repetitions if not job.is_forever else True:
                    await job.func(**job.kwargs)
                    await asyncio.sleep(job.interval_time.total_seconds())
                    number += 1
                self.jobs.remove(job)
