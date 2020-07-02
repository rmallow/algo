import action
import message as msg
from scheduler import scheduler
from asyncScheduler import asyncScheduler

class actionPool():
    def __init__(self, actions, feed, messageRouter, code):
        self.m_feed = feed
        self.m_messageRouter = messageRouter
        self.m_code = code
        self.m_events = []
        self.m_triggers = []
        for action in actions:
            if action.m_actionType == "event":
                self.m_events.append(action)
            else:
                self.m_triggers.append(action)

    def addAction(self, action):
        self.m_actions.append(action)

    def doActions(self, newData):
        for event in self.m_events:
            #get pandas columns, append it then add that to calculated feed
            cols = event.update(self.m_feed)
            self.m_feed.addNewCalcCols(cols)
        
        self.m_feed.appendCalcData()

        if len(self.m_triggers) > 0:
            self.m_messageRouter.receive(msg.message(msg.COMMAND_TYPE, msg.COMMAND_START,
            sourceCode=self.m_code))

            for trigger in self.m_triggers:
                messages = trigger.update(self.m_feed)
                for message in messages:
                    message.m_sourceCode = self.m_code
                    self.m_messageRouter.receive(message)

            self.m_messageRouter.receive(msg.message(msg.COMMAND_TYPE, msg.COMMAND_END,
            sourceCode=self.m_code))
        
            