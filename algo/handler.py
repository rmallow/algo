import algo.message
class handler():
    def __init__(self, name, calcFunc):
        self.m_name = name
        self.m_calcFunc = calcFunc
        self.m_count = 0

        self.m_incomingMessages = {}
        self.m_data = None

    #called by handlerManager to update on message list
    def update(self, code):
        msgLst = self.m_incomingMessages.pop(code, [])
        for msg in msgLst:
            print(self.m_count)
            self.m_count +=1
            self.m_calcFunc(msg)

    #called by message router to get message
    def receive(self, message):
        lst = self.m_incomingMessages.get(message.m_sourceCode, [])
        lst.append(message)
        self.m_incomingMessages[message.m_sourceCode] = lst