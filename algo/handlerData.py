from . import message

"""
mostly a wrapper for a two layered dict to make things 

NOT thread safe
"""
class handlerData():
    def __init__(self):
        self.m_dataSet = {}

    def __insert__(self, message):
        if message is not None and message.keyExists():
            key = message.m_key
            if key.m_sourceCode not in self.m_dataSet:
                self.m_dataSet[key.m_sourceCode] = {}
            
            if key.m_time not in self.m_dataSet[key.m_sourceCode]:
                self.m_dataSet[key.m_sourceCode][key.m_time] = []

            self.m_dataSet[key.m_sourceCode][key.m_time].append(message)

    """
    insert one message or list of messages
    """
    def insert(self, rawMessage):
        try:
            for msg in rawMessage:
                self.__insert__(msg)
        except TypeError:
            self.__insert__(rawMessage)        
            
