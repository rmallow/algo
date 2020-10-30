COMMAND_TYPE = 1
TRIGGER_TYPE = 2

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