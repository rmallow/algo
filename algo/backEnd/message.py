from enum import Enum
from dataclasses import dataclass
from .messageKey import messageKey

import typing


class MessageType(Enum):
    COMMAND = 1
    NORMAL = 2
    PRIORITY = 3
    UI_UPDATE = 4


class CommandType(Enum):
    START = 1
    END = 2
    ABORT = 3
    RESUME = 4
    CLEAR = 5


@dataclass
class message:
    messageType: MessageType
    content: typing.Any
    name: str = ""
    sourceName: str = ""
    key: messageKey = messageKey

    def keyExists(self):
        return self.key.sourceCode is not None and self.key.time is not None

    def isPriority(self):
        return self.type == MessageType.PRIORITY

    def isCommand(self):
        return self.type == MessageType.COMMAND

    def isNormal(self):
        return self.type == MessageType.NORMAL
