class ModuleNCounter:
    def __init__(self, n: int):
        self._value = 0

        if n <= 0:
            raise ValueError('N must be a integer greater than 1')
        self._n = n

    def increment(self):
        self._value = (self._value + 1) % self._n

    def reset(self):
        self._value = 0

    def get_value(self) -> int:
        return self._value
