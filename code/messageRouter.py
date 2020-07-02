import multiprocessing as mp
import queue
import message
import handler
import logging
import handlerManager


"""
This class works as an intermediate between the blocks and the handlers
The message router accepts new messages from triggers and sends
those messages out to all handlers that are subscribed to that message

after initialization, handler manager must be set
"""
class messageRouter():
    def __init__(self, handlerManager):
        self.m_end = False
        self.m_messageQueue = mp.Queue()
        self.m_handlerUpdateDict = {}
        self.m_handlerManger = handlerManager

    #send to message subscriptions
    def broadcast(self, message):
        handlerList = self.m_handlerManager.m_messageSubscriptions.get(message.m_name, [])
        updateSet = self.m_handlerUpdateDict.get(message.m_sourceCode, set())
        for handler in handlerList:
            handler.receive(message)
            updateSet.add(handler)

    def receive(self, message):
        self.m_messageQueue.put(message)

    #this will handle how the message router responds to various commands
    def processCommand(self, message):
        self.CMD_DICT.get(message.m_message,cmdNotFound)(self,message)
        
    def start(self):
        while not self.m_end:
            try:
                message = self.m_messageQueue.get(timeout=2)
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
        updateSet = self.m_handlerUpdateDict.pop(message.m_sourceCode,None)
        if updateSet is not None:
            #send to handlerManager queue
            val = (message.m_sourceCode, updateSet)

        else:
            logging.warning("end cmd on not found code:")
            logging.warning(str(message.m_sourceCode))

    def cmdAbort(self, message):
        pass

    def cmdResume(self, message):
        pass

    CMD_DICT = {
        message.COMMAND_START: cmdStart,
        message.COMMAND_END: cmdEnd,
        message.COMMAND_END: cmdAbort,
        message.COMMAND_RESUME: cmdResume
    }