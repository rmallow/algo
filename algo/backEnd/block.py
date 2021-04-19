from .actionPool import actionPool
from . import message as msg
from . import messageKey as msgKey
from . import constants as con

from .util.commandProcessor import commandProcessor

from ..commonUtil import errorHandling

import pandas as pd
import time


class block(commandProcessor):
    def __init__(self, actionList, feed, messageRouter, libraries, config, parseSettings=None, name="defaultBlockName",
                 code=123, **kwargs):
        self.code = code
        self.end = False
        self.keepUpdating = True
        self.feed = feed
        self.messageRouter = messageRouter
        self.pool = actionPool(actionList, feed, messageRouter, self.code, libraries, parseSettings)
        self.config = config
        self.mainframeQueue = None
        self.blockQueue = None

    def start(self):
        if self.mainframeQueue is not None:
            self.mainframeQueue.put("Starting " + self.code)

        while not self.end:
            if self.keepUpdating:
                newData = self.feed.update()
                if newData is not None:
                    if isinstance(newData, pd.DataFrame):
                        mainframeMessage = str(newData.index[0]) + " : " + str(newData.iloc[0].iloc[0])
                        self.mainframeQueue.put(mainframeMessage)
                        self.pool.doActions(newData)
                    elif newData == con.DataSourceReturnEnum.OUTSIDE_CONSTRAINT:
                        self.clear()
                    elif newData == con.DataSourceReturnEnum.NO_DATA:
                        # Want to do nothing and process potential block messages
                        pass
                    elif newData != con.DataSourceReturnEnum.END_DATA:
                        # Feed is at end of data so don't want to keep calling it
                        self.keepUpdating = False
                else:
                    # Feeds should not be returning None, issue a warning and stop updating
                    errorHandling.warning("Block " + str(self.code) + " received none data",
                                          description="Return END_DATA if feed is at end, not None")
                    self.keepUpdating = False

            # Check if there are messages for the block to process
            if self.blockQueue is not None:
                # This will block the block until the queue is cleared so need to avoid
                # spamming this with commands
                while not self.blockQueue.empty():
                    # Use the command processor way of handling command messages
                    commandMessage = self.m_blockQueue.get()
                    if commandMessage.messageType == msg.MessageType.COMMAND:
                        self.processCommand(commandMessage.content)

                # If there is no messages to get but we're also not getting any
                # more data from the feed then sleep a bit
                # third of a second seems reasonable as we're just waiting for input
                if self.blockQueue.empty() and not self.keepUpdating:
                    time.sleep(.3)

        # Return some data at the end
        return(self.feed.data, self.feed.calcData)

    def clear(self):
        self.feed.clear()
        # time is set as None as it won't be needed by message router
        message = msg.message(msg.MessageType.COMMAND, msg.CommandType.CLEAR,
                              key=msgKey.messageKey(self.code, None))
        self.messageRouter.receive(message)
