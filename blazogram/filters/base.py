from abc import ABC, abstractmethod


class BaseFilter(ABC):
    @abstractmethod
    async def __check__(self, update) -> bool:
        pass