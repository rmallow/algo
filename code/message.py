class message():
    COMMAND_TYPE = "COMMAND"
    TRIGGER_TYPE = "TRIGGER"
    
    def __init__(self, messageType, message, source = None):
        self.m_type = messageType
        self.m_message = message
        self.m_source = source