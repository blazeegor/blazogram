from .base import BaseSchedulerStorage, Job


class MemoryJobsStorage(BaseSchedulerStorage):
    def __init__(self):
        self.jobs: list[Job] = []

    async def add_job(self, job: Job):
        self.jobs.append(job)

    async def get_jobs(self) -> list[Job]:
        return self.jobs

    async def remove_jobs(self):
        self.jobs.clear()