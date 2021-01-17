from . import message

import logging

"""
Stores messages with by keys for handlers to acess quickly

code1:
{
    time1: (0, [data])
    time2: (1, [data])
    time3: (2, [data])
}
code2:
{
    time1: (0, [data])
    time2: (1, [data])
}

"""

class handlerData():
    def __init__(self):
        self.m_dataSet = {}

    """
    @brief: internal method to insert into handler data

    @param: message - must be of message data type!
    """
    def _insert(self, message):
        if message is not None and message.keyExists():
            key = message.m_key
            if key.m_sourceCode not in self.m_dataSet:
                self.m_dataSet[key.m_sourceCode] = {}
            
            if key.m_time not in self.m_dataSet[key.m_sourceCode]:
                indexAndData = (len(self.m_dataSet[key.m_sourceCode]),[])
                self.m_dataSet[key.m_sourceCode][key.m_time] = indexAndData

            self.m_dataSet[key.m_sourceCode][key.m_time][1].append(message)

    """
    insert one message or list of messages
    """
    def insert(self, rawMessage):
        try:
            for msg in rawMessage:
                self._insert(msg)
        except TypeError:
            self._insert(rawMessage)

    def _getCodeDict(self, key):
        try:
            return self.m_dataSet[key.m_sourceCode]
        except:
            logging.warning("invalid code for handler data access")
            return None

    def _getTimeData(self, key):
        codeDict = self._getCodeDict(key)

        if codeDict is None:
            return None

        try:
            #the first element is the index of the time, so return the data at second element
            return codeDict[key.m_time]
        except:
            logging.warning("invalid time for handler data access")
            return None

    def get(self, key, default = None):
        timeData = self._getTimeData(key)
        if timeData is not None:
            return timeData[1]
        else:
            return default

    def getPeriod(self, key, period):
        codeDict = self._getCodeDict(key)
        timeData = self._getTimeData(key)

        if timeData is None:
            return None

        timeEndIndex = timeData[0]
        timeStartIndex = 0
        if timeEndIndex < period or len(codeDict) < period:
            timeStartIndex = 0
        else:
            timeStartIndex = timeEndIndex - period

        keys = list(codeDict.keys())[timeStartIndex:timeEndIndex]

        #generate new dict and return using these keys, leaving out index
        return dict((k, codeDict[k][1]) for k in keys if k in codeDict)
        
            
    def clearCode(self, code):
        self.m_dataSet.pop(code,None)
