from . import message as msg
from .commandProcessor import commandProcessor
from .asyncScheduler import asyncScheduler

import queue
import logging
from collections.abc import Iterable


class messageRouter(commandProcessor):
    """
    This class works as an intermediate between the blocks and the handlers
    The message router accepts new messages from triggers and sends
    those messages out to all handlers that are subscribed to that message
    """
    def __init__(self, messageSubscriptions, handlerData, queue):
        # initalize command processor
        super().__init__()

        self.m_end = False
        self.m_messageQueue = queue
        self.m_messageSubscriptions = messageSubscriptions
        self.m_handlerUpdateDict = {}
        self.m_handlerData = handlerData

        self.m_blocksToClear = set()

        self.addCmdFunc(msg.CommandType.CLEAR, messageRouter.cmdClear)

        self.m_loop = asyncScheduler()
        self.m_process = None

    """
    def start(self):
        self.m_process = Process(target=self.initAndStartLoop, name="Router")
        self.m_process.start()
    """

    def initAndStartLoop(self):
        self.m_loop.init()
        self.m_loop.addTask(self.loop(), name="Router Main Loop")
        self.m_loop.start()
    
    """
    def join(self):
        self.m_process.join()
        self.m_loop.end()
    """

    async def loop(self):
        # main process loop for message router
        while not self.m_end:
            try:
                # pylint: disable=no-member
                message = await self.m_messageQueue.coro_get(timeout=2)
            except queue.Empty:
                continue
            else:
                if message is not None:
                    # determine if message is a command
                    if isinstance(message, msg.message):
                        # just one message, check what type
                        if message.isCommand():
                            # calls processorCommand func
                            self.processCommand(message)
                        elif message.isPriority():
                            # immediately broadcast a priority message
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

    # send to message subscriptions priority
    def broadcastPriority(self, message):
        self.m_handlerData.insert(message)
        handlerList = self.m_messageSubscriptions.get(message.m_name, [])
        for handlerToUpdate in handlerList:
            self.m_loop.addTaskArgs(handlerToUpdate.updatePriority, message)

    # send to message subscriptions
    def broadcast(self, message):
        self.m_handlerData.insert(message)
        handlerList = self.m_messageSubscriptions.get(message.m_name, [])
        updateSet = self.m_handlerUpdateDict.get(message.m_key, set())
        updateSet.update(handlerList)

    def receive(self, message):
        # pylint: disable=no-member
        self.m_messageQueue.put(message)

    def cmdStart(self, message):
        """
        @brief: called from command processor super class when Start command is received
            signals the start of messages for this key
            clears data for code if it's been marked to clear

        @param: message - command message
        """
        if message.m_key.m_sourceCode in self.m_blocksToClear:
            self.m_handlerData.clearCode(message.m_key.m_sourceCode)
            self.m_blocksToClear.remove(message.m_key.m_sourceCode)
        if message.m_key not in self.m_handlerUpdateDict:
            self.m_handlerUpdateDict[message.m_key] = set()
        else:
            logging.warning("start cmd on existing update list, code:")
            logging.warning(str(message.m_sourceCode))

    def cmdEnd(self, message):
        """
        @brief: called from command processor super class when End command is received
            signals the end of messages for this key

        @param: message - command message
        """
        updateSet = self.m_handlerUpdateDict.pop(message.m_key, set())
        for handlerToUpdate in updateSet:
            self.m_loop.addTaskArgs(handlerToUpdate.update, message.m_key)

    def cmdAbort(self, message):
        """
        @brief: called from command processor super class when Abort command is received

        @param: message - command message
        """
        self.m_end = True

    def cmdResume(self, message):
        """
        @brief: called from command processor super class when Resume command is received

        @param: message - command message
        """
        self.m_end = False

    def cmdClear(self, message):
        """
        @brief: called from command processor super class when Clear command is received
            Adds code to set, this code will be cleared when start is called for same code

        @param: message - command message
        """
        self.m_blocksToClear.add(message.m_key.m_sourceCode)
