import multiprocessing as mp
import queue
import message
import handler
import logging


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
        self.m_handlerUpdateDict = {}

    #send to message subscriptions
    def broadcast(self, message):
        handlerList = self.m_messageSubscriptions.get(message.m_name, [])
        for handler in handlerList:
            handler.send(message)

    def send(self, message):
        self.m_messageQueue.put(message)

    #this will handle how the message router responds to various commands
    def processCommand(self, message):
        self.CMD_DICT.get(message.m_message,cmdNotFound)(self,message)
        
    def start(self):
        while not self.m_end:
            try:
                message = self.m_messageQueue.get()
            except queue.Empty:
                pass
            else:
                if message is not None:
                    #determine if message is a command
                    if message.m_type is "command":
                        self.processCommand(message)
                    else:
                        self.broadcast(message)

    def cmdNotFound(self, message):
        logging.warning("unrecognized command")
        logging.warning(str(message.m_message))

    def cmdStart(self, message):
        if message.m_sourceCode not in self.m_handlerUpdateDict:
            self.m_handlerUpdateDict = []
        else:
            logging.warning("start cmd on existing update list, code:")
            logging.warning(str(message.m_sourceCode))

    def cmdEnd(self, message):
        updateList = self.m_handlerUpdateDict.pop(message.m_sourceCode.None)
        if updateList is not None:
            for handler in updateList:
                handler.update()
        else:
            logging.warning("end cmd on not found code:")
            logging.warning(str(message.m_sourceCode))

    def cmdAbort(self, message):
        pass

    def cmdResume(self, message):
        pass

    CMD_DICT = {
        101: cmdStart,
        102: cmdEnd,
        103: cmdAbort,
        104: cmdResume
    }