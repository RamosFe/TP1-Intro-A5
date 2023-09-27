class ModuleNCounter:
    """
    Represents a modulo-N counter.

    Args:
        n (int): The modulo value. Must be an integer greater than 1.

    Attributes:
        _value (int): The current counter value.
        _n (int): The modulo value.
    """

    def __init__(self, n: int):
        self._value = 0

        if n <= 1:
            raise ValueError("N must be an integer greater than 1")
        self._n = n

    def increment(self):
        """
        Increment the counter value and wrap around if it reaches the modulo value.
        """
        self._value = self.next()

    def reset(self):
        """Reset the counter value to 0."""
        self._value = 0

    def get_value(self) -> int:
        """
        Get the current counter value.

        Returns:
            int: The current counter value.
        """
        return self._value

    def next(self) -> int:
        return (self._value + 1) % self._n