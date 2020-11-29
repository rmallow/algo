import algo.messageKey


COMMAND_TYPE = 1
NORMAL_TYPE = 2
PRIORITY_TYPE = 3

COMMAND_START = 101
COMMAND_END = 102
COMMAND_ABORT = 103
COMMAND_RESUME = 104

class message():
    def __init__(self, messageType, message, name = None, sourceName = None, key = None):
        self.m_type = messageType
        self.m_message = message
        self.m_name = name
        self.m_sourceName = sourceName
        self.m_key = key

    def keyExists(self):
        return self.m_key.m_sourceCode is not None and self.m_key.m_time is not None

    def isPriority(self):
        return self.m_type == PRIORITY_TYPE

    def isCommand(self):
        return self.m_type == COMMAND_TYPE

    def isNormal(self):
        return self.m_type == NORMAL_TYPE
        