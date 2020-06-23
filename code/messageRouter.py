from multiprocessing import Queue

class messageRouter():
    def __init__(self):
        self.m_messageQueue = Queue()
        self.m_messageSubscriptions = {}

    def broadcast(self):
        x = 2
        #do something with Queue here