from .base import BaseSchedulerStorage
from ...database.sqlite import SQLite3
from .base import Job
import asyncio
import json
from datetime import datetime, timedelta


class SQLiteStorage(BaseSchedulerStorage):
    def __init__(self, database: SQLite3):
        self.database = database
        asyncio.create_task(self.start())

    async def start(self):
        await self.database.request('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, func TEXT, run_date INTEGER, number_repetitions INTEGER, interval_time INTEGER, is_forever TEXT, kwargs TEXT)')

    async def add_job(self, job: Job):
        await self.database.request('INSERT OR IGNORE INTO jobs (func, run_date, number_repetitions, interval_time, is_forever, kwargs) VALUES (?, ?, ?, ?, ?, ?)', (job.func, job.run_date.timestamp(), job.number_repetitions, job.interval_time.total_seconds(), str(job.is_forever), json.dumps(job.kwargs)))

    async def get_jobs(self) -> list[Job]:
        result = await self.database.select(table='jobs', columns=['func', 'run_date', 'number_repetitions', 'interval_time', 'is_forever', 'kwargs'])
        jobs = [Job(func=job[0], run_date=datetime.fromtimestamp(job[1]), number_repetitions=job[2], interval_time=timedelta(seconds=job[3]), is_forever=True if job[4] == 'True' else False, kwargs=json.loads(job[5])) for job in result]
        return jobs

    async def remove_jobs(self):
        await self.database.request('DELETE FROM jobs')