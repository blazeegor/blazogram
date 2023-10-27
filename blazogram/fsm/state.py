class State:
    def __init__(self, name: str):
        self.name = name
        self.data = {}

    def update_data(self, **kwargs):
        self.data.update(kwargs)

    def __str__(self):
        return self.name
