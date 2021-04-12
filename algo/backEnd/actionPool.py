from . import message as msg
from .messageKey import messageKey

from collections.abc import Iterable


class actionPool():
    """
    @brief: container and caller for all actions of a block, communicates with messageRouter

    __init__:
    @param: actions     - contains all valid actions of block
    @param: period      - refers to number of units, not time
    @param: name        - name of action
    @param: calcFunc    - passed in function that will be called on the dataSet
    @param: params      - extra parameters that are passed in each time to the calcFunc
    @param: inputCols   - the columns that are used by the action and put into the dataSet
    """
    def __init__(self, actions, feed, messageRouter, code, libraries, parseSettings=None):
        self.feed = feed
        self.messageRouter = messageRouter
        self.code = code
        self.events = []
        self.triggers = []

        # TODO: Finish requiremental setup and include here

        for action in actions:
            self.addAction(action)

    def addAction(self, action):
        if action.actionType == "event":
            self.events.append(action)
        else:
            self.triggers.append(action)

    def doActions(self, newData):
        if newData.empty:
            return
        for event in self.events:
            # get pandas columns, append it then add that to calculated feed
            event.update(self.feed)

        self.feed.appendCalcData()

        if len(self.triggers) > 0:

            # tell message router tha triggers are going to start sending messages
            startKey = messageKey(self.code, self.feed.newData.index[0])
            startCmd = msg.message(msg.MessageType.COMMAND, msg.CommandType.START, key=startKey)
            self.messageRouter.receive(startCmd)

            #
            #   various checks done on how to handle values/messages returned from trigger funcs
            #
            sentMessageList = []
            for trigger in self.triggers:
                rawTriggerValue = trigger.update(self.feed)
                if rawTriggerValue is not None:
                    if isinstance(rawTriggerValue, Iterable) and not isinstance(rawTriggerValue, str):
                        for rawMessage in rawTriggerValue:
                            sentMessage = None
                            if isinstance(rawMessage, msg.message):
                                # rawMessage are already message class messages
                                sentMessage = rawMessage
                                if sentMessage.key is None:
                                    sentMessage.key = startKey
                                sentMessage.name = trigger.name
                            else:
                                if rawMessage is None:
                                    continue
                                sentMessage = msg.message(msg.MessageType.NORMAL, rawMessage,
                                                          key=startKey, name=trigger.name)

                            if sentMessage.isPriority():
                                self.messageRouter.receive(sentMessage)
                            else:
                                sentMessageList.append(sentMessage)
                    elif isinstance(rawTriggerValue, msg.message):
                        # rawMessage are already message class messages
                        sentMessage = rawTriggerValue
                        if sentMessage.key is None:
                            sentMessage.key = startKey
                        sentMessage.name = trigger.name
                        if sentMessage.isPriority():
                            self.messageRouter.receive(sentMessage)
                        else:
                            sentMessageList.append(sentMessage)
                    else:
                        sentMessage = msg.message(msg.MessageType.NORMAL, rawTriggerValue,
                                                  key=startKey, name=trigger.name)
                        sentMessageList.append(sentMessage)

            # send all the non priority messages
            self.messageRouter.receive(sentMessageList)
            #
            #   End of trigger func updating and sending to message router
            #
            # tell message router tha triggers are going to done sending messages
            # handlers should now be told to process this block of messages

            endKey = messageKey(self.code, self.feed.newData.index[-1])
            endCmd = msg.message(msg.MessageType.COMMAND, msg.CommandType.END, key=endKey)
            self.messageRouter.receive(endCmd)

    def sendAbortCommand(self):
        message = msg.message(msg.MessageType.COMMAND, msg.CommandType.ABORT)
        self.messageRouter.receive(message)
