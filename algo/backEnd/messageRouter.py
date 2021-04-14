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

        self.end = False
        self.messageQueue = queue
        self.messageSubscriptions = messageSubscriptions
        self.handlerUpdateDict = {}
        self.handlerData = handlerData

        self.blocksToClear = set()

        self.addCmdFunc(msg.CommandType.CLEAR, messageRouter.cmdClear)

        self.loop = asyncScheduler()

    def initAndStartLoop(self):
        self.loop.init()
        self.loop.addTask(self.mainLoop(), name="Router Main Loop")
        self.loop.start()

    async def mainLoop(self):
        # main process loop for message router
        while not self.end:
            try:
                # pylint: disable=no-member
                message = await self.messageQueue.coro_get(timeout=2)
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
        self.handlerData.insert(message)
        handlerList = self.messageSubscriptions.get(message.name, [])
        for handlerToUpdate in handlerList:
            self.loop.addTaskArgs(handlerToUpdate.updatePriority, message)

    # send to message subscriptions
    def broadcast(self, message):
        self.handlerData.insert(message)
        handlerList = self.messageSubscriptions.get(message.name, [])
        updateSet = self.handlerUpdateDict.get(message.key, set())
        updateSet.update(handlerList)

    def receive(self, message):
        # pylint: disable=no-member
        self.messageQueue.put(message)

    def cmdStart(self, message):
        """
        @brief: called from command processor super class when Start command is received
            signals the start of messages for this key
            clears data for code if it's been marked to clear

        @param: message - command message
        """
        if message.key.sourceCode in self.blocksToClear:
            self.handlerData.clearCode(message.key.sourceCode)
            self.blocksToClear.remove(message.key.sourceCode)
        if message.key not in self.handlerUpdateDict:
            self.handlerUpdateDict[message.key] = set()
        else:
            logging.warning("start cmd on existing update list, code:")
            logging.warning(str(message.sourceCode))

    def cmdEnd(self, message):
        """
        @brief: called from command processor super class when End command is received
            signals the end of messages for this key

        @param: message - command message
        """
        updateSet = self.handlerUpdateDict.pop(message.key, set())
        for handlerToUpdate in updateSet:
            self.loop.addTaskArgs(handlerToUpdate.update, message.key)

    def cmdAbort(self, message):
        """
        @brief: called from command processor super class when Abort command is received

        @param: message - command message
        """
        self.end = True

    def cmdResume(self, message):
        """
        @brief: called from command processor super class when Resume command is received

        @param: message - command message
        """
        self.end = False

    def cmdClear(self, message):
        """
        @brief: called from command processor super class when Clear command is received
            Adds code to set, this code will be cleared when start is called for same code

        @param: message - command message
        """
        self.blocksToClear.add(message.key.sourceCode)
