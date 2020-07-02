import message
class handler():
    def __init__(self, name, calcFunc):
        self.m_name = name
        self.m_calcFunc = calcFunc

        self.m_incomingMessages = {}
        self.m_data = None

    #called by messageRouter if there is an incoming message
    def update(self, code):
        msgLst = self.m_incomingMessages.pop(code, [])
        for msg in msgLst:
            self.m_calcFunc(msg)

    def recieve(self, message):
        lst = self.m_incomingMessages.get(message.m_sourceCode, [])
        lst.append(message)
        self.m_incomingMessages[message.m_sourceCode] = lst