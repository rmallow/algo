from .actionPool import actionPool
from . import message as msg
from . import messageKey as msgKey
from . import constants as con

from .util.commandProcessor import commandProcessor

from ..commonUtil import mpLogging
from ..commonUtil.helpers import getStrTime
from ..commonGlobals import BLOCK_GROUP, SEND_TIME, RECEIVE_TIME, NOT_AVAIL_STR

import pandas as pd
import threading
import time


BLOCK_QUEUE_CHECK_TIMER = .5


class block(commandProcessor):
    def __init__(self, actionList, feed, messageRouter, libraries, config, *args, parseSettings=None,
                 name="defaultBlockName", code=123, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code
        self.end = False
        self.keepUpdating = True
        self.feed = feed
        self.messageRouter = messageRouter
        self.pool = actionPool(actionList, feed, messageRouter, self.code, libraries, parseSettings)
        self.config = config
        self.mainframeQueue = None
        self.blockQueue = None
        self.track = False
        self.feedLastUpdateTime = 0

        self.addCmdFunc(msg.CommandType.ADD_OUTPUT_VIEW, block.addOutputView)
        self.addCmdFunc(msg.CommandType.CHECK_STATUS, block.checkStatus)

    def checkBlockQueue(self):
        # Check if there are messages for the block to process
        if self.blockQueue is not None:
            # This will block the block until the queue is cleared so need to avoid
            # spamming this with commands
            while not self.blockQueue.empty():
                # Use the command processor way of handling command messages
                commandMessage = self.blockQueue.get()
                if commandMessage.messageType == msg.MessageType.COMMAND:
                    self.processCommand(commandMessage.content, details=commandMessage.details)
        # schedule it again after the timer
        threading.Timer(BLOCK_QUEUE_CHECK_TIMER, self.checkBlockQueue).start()

    def start(self):
        if self.mainframeQueue is not None:
            self.mainframeQueue.put("Starting " + self.code)

        threading.Timer(BLOCK_QUEUE_CHECK_TIMER, self.checkBlockQueue).start()

        while not self.end:
            if self.keepUpdating:
                newData = self.feed.update()
                self.feedLastUpdateTime = time.time()
                if newData is not None:
                    if isinstance(newData, pd.DataFrame):
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
                    mpLogging.warning("Block " + str(self.code) + " received none data", group=BLOCK_GROUP,
                                      description="Return END_DATA if feed is at end, not None")
                    self.keepUpdating = False

            if self.track:
                calcTail = self.feed.calcData.tail(len(self.feed.newData))
                dataTail = self.feed.data.tail(len(self.feed.newData))
                combinedDf = pd.concat([dataTail, calcTail], axis=1)
                m = msg.message(msg.MessageType.UI_UPDATE, content=msg.UiUpdateType.BLOCK, details=combinedDf,
                                key=msgKey.messageKey(self.code, combinedDf.index[0]))
                self.mainframeQueue.put(m)

        # Return some data at the end
        return(self.feed.data, self.feed.calcData)

    def clear(self):
        self.feed.clear()
        # time is set as None as it won't be needed by message router
        message = msg.message(msg.MessageType.COMMAND, msg.CommandType.CLEAR,
                              key=msgKey.messageKey(self.code, None))
        self.messageRouter.receive(message)

    def addOutputView(self, _, _2):
        self.track = True

    def checkStatus(self, _, details):
        returnMessage = msg.message(msg.MessageType.UI_UPDATE, msg.UiUpdateType.STATUS,
                                    key=msgKey.messageKey(self.code, None), details={})
        sendTime = NOT_AVAIL_STR
        if details is not None and isinstance(details, dict):
            if SEND_TIME in details:
                sendTime = details[SEND_TIME]
        returnMessage.details[SEND_TIME] = sendTime
        returnMessage.details[RECEIVE_TIME] = getStrTime(time.time())
        feedLength = 0
        if self.feed.data is not None:
            feedLength = len(self.feed.data.index)
        returnMessage.details["Data length"] = str(feedLength)
        returnMessage.details["Feed last update time"] = getStrTime(self.feedLastUpdateTime)
        self.mainframeQueue.put(returnMessage)
