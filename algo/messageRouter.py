import algo.message
import algo.messageKey
import algo.handlerAsync
import algo.message as msg
from algo.commandProcessor      import commandProcessor
from algo.handlerData           import handlerData
from algo.asyncScheduler        import asyncScheduler

import aioprocessing
import multiprocessing as mp
import queue
import logging
from collections.abc import Iterable

"""
This class works as an intermediate between the blocks and the handlers
The message router accepts new messages from triggers and sends
those messages out to all handlers that are subscribed to that message
"""
class messageRouter(commandProcessor):
    def __init__(self, messageSubscriptions, handlerData):
        #initalize command processor
        super().__init__()
        
        self.m_end = False
        self.m_messageQueue = aioprocessing.AioQueue()
        self.m_messageSubscriptions = messageSubscriptions
        self.m_handlerUpdateDict = {}
        self.m_handlerData = handlerData

        self.m_loop = asyncScheduler()

    #send to message subscriptions priority
    def broadcastPriority(self, message):
        self.m_handlerData.insert(message)
        handlerList = self.m_messageSubscriptions.get(message.m_name, [])
        for handlerToUpdate in handlerList:
            self.m_loop.addTaskArgs(handlerToUpdate.updatePriority, message)    
    
    #send to message subscriptions
    def broadcast(self, message):
        self.m_handlerData.insert(message)
        handlerList = self.m_messageSubscriptions.get(message.m_name, [])
        updateSet = self.m_handlerUpdateDict.get(message.m_key, set())
        updateSet.update(handlerList)

    def receive(self, message):
        # pylint: disable=no-member
        self.m_messageQueue.put(message)

    #calls initAndStart on loop with router as only object
    def initAndStart(self):
        self.m_loop.initAndStart(self)

    async def start(self):
        #main process loop for message router
        while not self.m_end:
            try:
                # pylint: disable=no-member
                message = await self.m_messageQueue.coro_get(timeout=2)
            except queue.Empty:
                continue
            else:
                if message is not None:
                    #determine if message is a command
                    if isinstance(message, msg.message):
                        #just one message, check what type
                        if message.isCommand():
                            #calls processorCommand func
                            self.processCommand(message)
                        elif message.isPriority():
                            #immediately broadcast a priority message
                            self.broadcastPriority(message)
                        else:
                            logging.warning("unexpected message type:")
                            logging.warning(str(message))
                    elif isinstance(message, Iterable):
                        for singleMessage in message:
                            if isinstance(singleMessage, msg.message) and singleMessage.isNormal():
                                self.broadcast(singleMessage)
                            else:
                                logging.warning("unexpected value in message router message list:")
                                logging.warning(str(singleMessage))
                    else:
                        logging.warning("unexpected value in message router")
                        logging.warning(str(message))


    def cmdStart(self, message):
        if message.m_key not in self.m_handlerUpdateDict:
            self.m_handlerUpdateDict[message.m_key] = set()
        else:
            logging.warning("start cmd on existing update list, code:")
            logging.warning(str(message.m_sourceCode))

    def cmdEnd(self, message):
        updateSet = self.m_handlerUpdateDict.pop(message.m_key,set())
        for handlerToUpdate in updateSet:
            self.m_loop.addTaskArgs(handlerToUpdate.update, message.m_key)
            
    def cmdAbort(self, message):
        self.m_end = True

    def cmdResume(self, message):
        self.m_end = False