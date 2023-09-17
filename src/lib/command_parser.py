from enum import Enum


class ClientOption(Enum):
    UPLOAD = 'UPLOAD'
    DOWNLOAD = 'DOWNLOAD'


class Command:
    def __init__(self, option: ClientOption, name: str, size: int):
        self.option = option
        self.name = name
        self.size = size

    def to_str(self) -> str:
        return f'{self.option.value}:{self.name}:{self.size}'

    @staticmethod
    def from_str(msg: str):
        parts = msg.split(':')
        option = ClientOption(parts[0])
        name = parts[1]
        size = int(parts[2])
        return Command(option, name, size)
