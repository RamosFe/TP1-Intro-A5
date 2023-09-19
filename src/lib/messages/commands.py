from enum import Enum


class MessageOption(Enum):
    UPLOAD = 'UPLOAD'
    DOWNLOAD = 'DOWNLOAD'
    LIST_FILES = 'LS'


class Command:
    def __init__(self, option: MessageOption, name: str, size: int):
        self.option = option
        self.name = name
        self.size = size

    def to_str(self) -> str:
        return f'{self.option.value}:{self.name}:{self.size}'

    @staticmethod
    def from_str(msg: str):
        
        print(f"msg:{msg}")
        parts = msg.split(':')
        option = MessageOption(parts[0])
        if option == MessageOption.LIST_FILES:
            return Command(option,None,None)
        name = parts[1]
        size = None   
        if option == MessageOption.UPLOAD:
            size = int(parts[2])
            print(size)
        return Command(option, name, size)


class CommandResponse:
    def __init__(self, msg: str):
        self._msg = msg

    def is_error(self) -> bool:
        return self._msg != 'OK'

    def to_str(self) -> str:
        return self._msg

    @staticmethod
    def ok_response():
        return CommandResponse('OK')

    @staticmethod
    def err_response(msg: str):
        return CommandResponse(msg)
