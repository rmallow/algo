
class handler():
    def __init__(self, name, calcFunc):
        self.m_name = name
        self.m_calcFunc = calcFunc

        self.m_incomingMessages = {}
        self.m_data = None

    #called by messageRouter if there is an incoming message
    def update(self, code):
        pass

    def recieve(self, message):
        pass
        