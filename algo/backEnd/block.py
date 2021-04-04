from .actionPool import actionPool
from . import message as msg
from . import messageKey as msgKey
from . import constants as con

from .commandProcessor import commandProcessor

import pandas as pd
import time


class block(commandProcessor):
    def __init__(self, actionList, feed, messageRouter, libraries, config, parseSettings=None, name="defaultBlockName",
                 code=123, **kwargs):
        self.m_code = code
        self.m_end = False
        self.m_keepUpdating = True
        self.m_feed = feed
        self.m_messageRouter = messageRouter
        self.m_pool = actionPool(actionList, feed, messageRouter, self.m_code, libraries, parseSettings)
        self.m_config = config
        self.m_mainframeQueue = None
        self.m_blockQueue = None

    def start(self):
        if self.m_mainframeQueue is not None:
            self.m_mainframeQueue.put("Starting " + self.m_code)

        while not self.m_end:
            if self.m_keepUpdating:
                newData = self.m_feed.update()
                if newData is not None:
                    if isinstance(newData, pd.DataFrame):
                        mainframeMessage = str(newData.index[0]) + " : " + str(newData.iloc[0].iloc[0].item())
                        self.m_mainframeQueue.put(mainframeMessage)
                        self.m_pool.doActions(newData)
                    elif newData == con.OUTSIDE_CONSTRAINT:
                        self.clear()
                else:
                    # Feed is at end of data so don't want to keep calling it
                    self.m_keepUpdating = False
            # Check if there are messages for the block to process
            if self.m_blockQueue is not None:
                # This will block the block until the queue is cleared so need to avoid
                # spamming this with commands
                while not self.m_blockQueue.empty():
                    # Use the command processor way of handling command messages
                    self.processCommand(self.m_blockQueue.get())

                # If there is no messages to get but we're also not getting any
                # more data from the feed then sleep a bit
                # third of a second seems reasonable as we're just waiting for input
                if self.m_blockQueue.empty() and not self.m_keepUpdating:
                    time.sleep(.3)

        # Return some data at the end
        return(self.m_feed.m_data, self.m_feed.m_calcData)

    def clear(self):
        self.m_feed.clear()
        # time is set as None as it won't be needed by message router
        message = msg.message(msg.MessageType.COMMAND, msg.CommandType.CLEAR,
                              key=msgKey.messageKey(self.m_code, None))
        self.m_messageRouter.receive(message)
