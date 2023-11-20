from dataclasses import dataclass
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


@dataclass
class Job:
    func: callable
    run_date: datetime
    number_repetitions: int
    interval_time: timedelta
    is_forever: bool
    kwargs: dict


class BaseSchedulerStorage(ABC):
    @abstractmethod
    async def add_job(self, job: Job):
        pass

    @abstractmethod
    async def get_jobs(self) -> list[Job]:
        pass

    @abstractmethod
    async def remove_jobs(self):
        pass
