from enum import Enum


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


class message():
    def __init__(self, messageType, message, name=None, sourceName=None, key=None):
        self.m_type = messageType
        self.m_message = message
        self.m_name = name
        self.m_sourceName = sourceName
        self.m_key = key

    def keyExists(self):
        return self.m_key.m_sourceCode is not None and self.m_key.m_time is not None

    def isPriority(self):
        return self.m_type == MessageType.PRIORITY

    def isCommand(self):
        return self.m_type == MessageType.COMMAND

    def isNormal(self):
        return self.m_type == MessageType.NORMAL
