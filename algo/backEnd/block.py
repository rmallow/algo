from .actionPool import actionPool
from . import message as msg
from . import messageKey as msgKey
from . import constants as con

from .commandProcessor import commandProcessor

import pandas as pd


class block(commandProcessor):
    def __init__(self, actionList, feed, messageRouter, libraries, config, parseSettings=None, name="defaultBlockName",
                 code=123):
        self.m_code = code
        self.m_end = False
        self.m_feed = feed
        self.m_messageRouter = messageRouter
        self.m_pool = actionPool(actionList, feed, messageRouter, self.m_code, libraries, parseSettings)
        self.m_config = config

    def start(self):
        while not self.m_end:
            newData = self.m_feed.update()
            if newData is not None:
                if isinstance(newData, pd.DataFrame):
                    self.m_pool.doActions(newData)
                elif newData == con.OUTSIDE_CONSTRAINT:
                    self.clear()
            else:
                self.m_end = True
        return(self.m_feed.m_data, self.m_feed.m_calcData)

    def clear(self):
        self.m_feed.clear()
        # time is set as None as it won't be needed by message router
        message = msg.message(msg.MessageType.COMMAND, msg.CommandType.CLEAR,
                              key=msgKey.messageKey(self.m_code, None))
        self.m_messageRouter.receive(message)