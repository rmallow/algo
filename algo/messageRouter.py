import multiprocessing as mp
import queue
import algo.message as msg
import algo.handler
import logging
import algo.handlerManager

"""
This class works as an intermediate between the blocks and the handlers
The message router accepts new messages from triggers and sends
those messages out to all handlers that are subscribed to that message
"""
class messageRouter():
    def __init__(self, handlerManager):
        self.m_end = False
        self.m_messageQueue = mp.Queue()
        self.m_handlerUpdateDict = {}
        self.m_handlerManager = handlerManager

    #send to message subscriptions
    def broadcast(self, message):
        handlerList = self.m_handlerManager.m_messageSubscriptions.get(message.m_name, [])
        updateSet = self.m_handlerUpdateDict.get(message.m_sourceCode, set())
        for handler in handlerList:
            handler.receive(message)
            updateSet.add(handler)

    def receive(self, message):
        self.m_messageQueue.put(message)

       
    def start(self):
        while not self.m_end:
            try:
                message = self.m_messageQueue.get(timeout=2)
            except queue.Empty:
                pass
            else:
                if message is not None:
                    #determine if message is a command
                    if message.m_type == msg.COMMAND_TYPE:

                        self.processCommand(message)
                    else:
                        self.broadcast(message)

    def cmdNotFound(self, message):
        logging.warning("unrecognized command")
        logging.warning(str(message.m_message))

    def cmdStart(self, message):
        if message.m_sourceCode not in self.m_handlerUpdateDict:
            self.m_handlerUpdateDict[message.m_sourceCode] = set()
        else:
            logging.warning("start cmd on existing update list, code:")
            logging.warning(str(message.m_sourceCode))

    def cmdEnd(self, message):
        updateSet = self.m_handlerUpdateDict.pop(message.m_sourceCode,None)
        if updateSet is not None:
            #send to handlerManager queue
            message = msg.message(msg.TRIGGER_TYPE, updateSet, sourceCode=message.m_sourceCode)
            self.m_handlerManager.receive(message)
        else:
            logging.warning("end cmd on not found code:")
            logging.warning(str(message.m_sourceCode))

    def cmdAbort(self, message):
        self.m_handlerManager.receive(message)
        self.m_end = True

    def cmdResume(self, message):
        pass

    def processCommand(self, message):
        self.CMD_DICT.get(message.m_message,self.cmdNotFound)(self,message)

    CMD_DICT = {
        msg.COMMAND_START: cmdStart,
        msg.COMMAND_END: cmdEnd,
        msg.COMMAND_ABORT: cmdAbort,
        msg.COMMAND_RESUME: cmdResume
    }