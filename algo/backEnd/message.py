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
    ADD_OUTPUT_VIEW = 6
    CHECK_STATUS = 7
    UI_STARTUP = 8


class UiUpdateType(Enum):
    OUTPUT = 1
    BLOCK = 2
    HANDLER = 3
    LOGGING = 4
    STATUS = 5


"""
Message type - determines what to do with message
Content - main part of message, such as command type or data
Details - extra supporting parts to message, stored outside content and not required
name    - name of message
sourceName  - name of source that sent message
key     - code and time of message
"""


@dataclass
class message:
    messageType: MessageType
    content: typing.Any
    details: typing.Any = None
    name: str = ""
    sourceName: str = ""
    key: messageKey = messageKey(None, None)

    def keyExists(self):
        return self.key.sourceCode is not None and self.key.time is not None

    def isPriority(self):
        return self.messageType == MessageType.PRIORITY

    def isCommand(self):
        return self.messageType == MessageType.COMMAND

    def isNormal(self):
        return self.messageType == MessageType.NORMAL

    def isUIUpdate(self):
        return self.messageType == MessageType.UI_UPDATE
