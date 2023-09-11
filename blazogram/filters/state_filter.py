from .base import BaseFilter
from ..fsm.state import State


class StateFilter(BaseFilter):
    def __init__(self, state: State):
        self.state_id = state.state_id

    async def __check__(self, state_id: int) -> bool:
        return self.state_id == state_id