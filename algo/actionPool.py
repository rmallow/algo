import algo.action
import algo.message as msg
from algo.asyncScheduler import asyncScheduler

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
            event.update(self.m_feed)
        
        self.m_feed.appendCalcData()

        if len(self.m_triggers) > 0:
            message = msg.message(msg.COMMAND_TYPE, msg.COMMAND_START, sourceCode=self.m_code)
            self.m_messageRouter.receive(message)

            for trigger in self.m_triggers:
                messages = trigger.update(self.m_feed)
                for message in messages:
                    message.m_sourceCode = self.m_code
                    self.m_messageRouter.receive(message)

            message = msg.message(msg.COMMAND_TYPE, msg.COMMAND_END, sourceCode=self.m_code)
            self.m_messageRouter.receive(message)

    def sendAbortCommand(self):
        message = msg.message(msg.COMMAND_TYPE, msg.COMMAND_ABORT)
        self.m_messageRouter.receive(message)
        
            