import random


class State:
    def __init__(self, name: str = f'state{random.randint(10000, 999999)}'):
        self.name = name

    def __str__(self) -> str:
        return self.name


class StatesGroup:
    def __init__(self, *states: State):
        self.states = list(states)
        self.states_iter = None

    def start(self) -> State:
        self.states_iter = iter(self.states)
        return self.states[0]

    def next(self) -> State:
        return self.states_iter.__next__()

    def get_state(self, name: str) -> State:
        for state in self.states:
            if state.name == name:
                return state

    def __str__(self) -> str:
        string = 'StatesGroup: '

        for state in self.states:
            string += state.name + ', '

        return string
