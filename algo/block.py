from .feed import feed
from .actionPool import actionPool
from . import message as msg
from . import messageKey as msgKey
from . import constants as con

import pandas as pd

class block():
    def __init__(self, actionList, feed, messageRouter, libraries, parseSettings = None, name ="defaultBlockName", code = 123):
        #somehow options for the feed need to be read in here, can be implemented later, for now set manually
        self.m_code = code
        self.m_end = False
        self.m_feed = feed
        self.m_messageRouter = messageRouter
        self.m_pool = actionPool(actionList, feed, messageRouter, self.m_code, libraries, parseSettings)

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

    def clear(self):
        self.m_feed.clear()
        #time is set as None as it won't be needed by message router
        message = msg.message(msg.MessageType.COMMAND, msg.CommandType.CLEAR,
            key=msgKey.messageKey(self.m_code, None) )
        self.m_messageRouter.receive(message)
