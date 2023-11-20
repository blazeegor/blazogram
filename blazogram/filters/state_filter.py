from .base import BaseFilter
from ..fsm.state import State


class StateFilter(BaseFilter):
    def __init__(self, state: State):
        self.state = state

    async def __check__(self, state: State) -> bool:
        check = self.state is State

        return check or self.state.name == state.name if state else check
