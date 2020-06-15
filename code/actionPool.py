import action
from scheduler import scheduler
from asyncScheduler import asyncScheduler

class actionPool():
    def __init__(self, actions, feed):
        self.m_actions = actions  #list of actions

    def addAction(self, action):
        self.m_actions.append(action)

    def doAction(self, newData):
        for action in self.m_actions:
            action.update((), newData)
            if hasattr(action, 'm_childBlock') and action.m_childBlock is not None:
                x = 2
                #add what to do for sub blocks here
