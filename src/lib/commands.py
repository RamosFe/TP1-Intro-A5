from enum import Enum


class MessageOption(Enum):
    UPLOAD = 'UPLOAD'
    DOWNLOAD = 'DOWNLOAD'


class Command:
    def __init__(self, option: MessageOption, name: str, size: int):
        self.option = option
        self.name = name
        self.size = size

    def to_str(self) -> str:
        return f'{self.option.value}:{self.name}:{self.size}'

    @staticmethod
    def from_str(msg: str):
        parts = msg.split(':')
        option = MessageOption(parts[0])
        name = parts[1]
        size = None   
        if option == MessageOption.UPLOAD:
            size = int(parts[2])
        return Command(option, name, size)


class CommandResponse:
    def __init__(self, msg: str):
        self._msg = msg

    def is_error(self) -> bool:
        return "ERR" in self._msg

    def to_str(self) -> str:
        return self._msg
    
    def size(self) -> int:
        if self.is_error() or "UPLOAD" not in self._msg:
            return -1
        return int(self._msg.split(':')[2])

    @staticmethod
    def ok_response():
        return CommandResponse('OK')

    @staticmethod
    def err_response(msg: str):
        return CommandResponse(msg)