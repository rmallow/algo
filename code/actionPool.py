import action
from scheduler import scheduler
from asyncScheduler import asyncScheduler

class actionPool():
    def __init__(self, actions, feed):
        self.m_feed = feed
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

        for trigger in self.m_triggers:
            trigger.update(self.m_feed)
        
            