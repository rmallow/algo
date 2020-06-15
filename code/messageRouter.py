from multiprocessing import Queue

class messageRouter():
    def __init__(self):
        self.m_messageQueue = Queue()
        self.m_messageSubscriptions = {}