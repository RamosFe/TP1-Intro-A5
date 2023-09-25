from enum import Enum
from typing import Optional


class MessageOption(Enum):
    """
    An enumeration representing message options for file transfer commands.

    Attributes:
        UPLOAD (str): Represents the "UPLOAD" option.
        DOWNLOAD (str): Represents the "DOWNLOAD" option.
    """
    UPLOAD = "UPLOAD"
    DOWNLOAD = "DOWNLOAD"


class Command:
    """
    A class representing a file transfer command.

    Args:
        option (MessageOption): The message option, either "UPLOAD" or "DOWNLOAD".
        name (str): The name of the file associated with the command.
        size (Optional[int]): The size of the file (only used for "UPLOAD" commands).

    Methods:
        to_str() -> str:
            Serialize the command object into a string.

        from_str(msg: str) -> Command:
            Deserialize a string message into a Command object.

    Attributes:
        option (MessageOption): The message option, either "UPLOAD" or "DOWNLOAD".
        name (str): The name of the file associated with the command.
        size (Optional[int]): The size of the file (only used for "UPLOAD" commands).
    """
    def __init__(self, option: MessageOption, name: str, size: Optional[int]):
        self.option = option
        self.name = name
        self.size = size

    def to_str(self) -> str:
        """Serialize the command object into a string."""
        return f"{self.option.value}:{self.name}:{self.size}"

    @staticmethod
    def from_str(msg: str) -> "Command":
        """Deserialize a string message into a Command object."""
        parts = msg.split(":")
        option = MessageOption(parts[0])
        name = parts[1]
        size = None
        if option == MessageOption.UPLOAD:
            size = int(parts[2])
        return Command(option, name, size)


class CommandResponse:
    """
    A class representing a response to a file transfer command.

    Args:
        msg (str): The response message.

    Methods:
        is_error() -> bool:
            Check if the response represents an error.

        to_str() -> str:
            Get the response message as a string.

        size() -> int:
            Get the size associated with the response (only used for "UPLOAD" responses).

    Attributes:
        _msg (str): The response message.
    """
    def __init__(self, msg: str):
        self._msg = msg

    def is_error(self) -> bool:
        """Check if the response represents an error."""
        return "ERR" in self._msg

    def to_str(self) -> str:
        """Get the response message as a string."""
        return self._msg

    def size(self) -> int:
        """Get the size associated with the response (only used for "UPLOAD" responses)."""
        if self.is_error() or "UPLOAD" not in self._msg:
            return -1
        return int(self._msg.split(":")[2])

    @staticmethod
    def ok_response() -> "CommandResponse":
        """Create an OK response."""
        return CommandResponse("OK")

    @staticmethod
    def err_response(msg: str) -> "CommandResponse":
        """Create an error response with a custom message."""
        return CommandResponse(msg)
