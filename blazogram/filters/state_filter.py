from ..fsm.state import State
from .base import BaseFilter


class StateFilter(BaseFilter):
    def __init__(self, state: State):
        self.state = state

    async def __check__(self, state: State) -> bool:
        return self.state is state