from enum import Enum
from dataclasses import dataclass

class MessageType(Enum):
    COMMAND = 1
    NORMAL = 2
    PRIORITY = 3


class CommandType(Enum):
    START = 1
    END = 2
    ABORT = 3
    RESUME = 4
    CLEAR = 5


@dataclass
class message:
    messageType: MessageType
    message: str
    name: str = ""
    sourceName: str = ""
    key: str = ""

    def keyExists(self):
        return self.key.sourceCode is not None and self.key.time is not None

    def isPriority(self):
        return self.type == MessageType.PRIORITY

    def isCommand(self):
        return self.type == MessageType.COMMAND

    def isNormal(self):
        return self.type == MessageType.NORMAL
