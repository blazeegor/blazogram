import random


class State:
    def __init__(self, name: str = f'state{random.randint(10000, 999999)}'):
        self.name = name

    def __str__(self) -> str:
        return self.name


class StatesGroup:
    def __init__(self, *states: State):
        self.states = iter(list(states))

    def start(self) -> State:
        return self.states.__next__()

    def next(self) -> State:
        return self.states.__next__()