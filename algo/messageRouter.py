
import algo.messageKey
from algo.commandProcessor import commandProcessor
import algo.handlerAsync

import multiprocessing as mp
import queue
import algo.message as msg
import logging

"""
This class works as an intermediate between the blocks and the handlers
The message router accepts new messages from triggers and sends
those messages out to all handlers that are subscribed to that message
"""
class messageRouter(commandProcessor):
    def __init__(self, messageSubscriptions):
        self.m_end = False
        self.m_messageQueue = mp.Queue()
        self.m_messageSubscriptions = messageSubscriptions
        self.m_handlerUpdateDict = {}

    #send to message subscriptions
    def broadcast(self, message):
        handlerList = self.m_messageSubscriptions.get(message.m_name, [])
        updateSet = self.m_handlerUpdateDict.get(message.m_key, set())
        updateSet.update(handlerList)

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
                        #calls processorCommand func
                        self.processCommand(message)
                    else:
                        self.broadcast(message)

    def cmdStart(self, message):
        if message.m_key not in self.m_handlerUpdateDict:
            self.m_handlerUpdateDict[message.m_key] = set()
        else:
            logging.warning("start cmd on existing update list, code:")
            logging.warning(str(message.m_sourceCode))

    def cmdEnd(self, message):
        updateSet = self.m_handlerUpdateDict.pop(message.m_key,set())
        for handlerToUpdate in updateSet:
            handlerToUpdate.coroReceiveCommand(message)
            
    def cmdAbort(self, message):
        self.m_end = True

    def cmdResume(self, message):
        self.m_end = False