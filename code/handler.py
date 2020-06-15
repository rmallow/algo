
class handler():
    def __init__(self, tradeFunc, messageRouter):
        self.m_tradeFunc = tradeFunc
        self.m_messageRouter = messageRouter

    def getMessage(self):
        x = 2
        