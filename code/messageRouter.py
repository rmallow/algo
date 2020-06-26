import multiprocessing as mp
import queue


"""
This class works as an intermediate between the blocks and the handlers
The message router accepts new messages from triggers and sends
those messages out to all handlers that are subscribed to that message
"""
class messageRouter():
    def __init__(self):
        self.m_end = False
        self.m_messageQueue = mp.Queue()
        self.m_messageSubscriptions = {}

    #send to message subscriptions
    def broadcast(self, message):
        handlerList = self.m_messageSubscriptions.get(message.m_name, [])
        for handler in handlerList:
            handler.send(message)

    def send(self, message):
        self.m_messageQueue.put(message)

    def start(self):
        while not self.m_end:
            try:
                message = self.m_messageQueue.get()
                if message is not None:
                    self.broadcast(message)
            except queue.Empty:
                pass
