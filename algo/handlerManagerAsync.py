from .handlerAsync import handler
from .asyncScheduler import asyncScheduler
from .message import message as msg

import multiprocessing as mp
import importlib
import queue
import logging

def _loadCalcFunc(calcFuncConfig):
    return getattr(importlib.import_module(calcFuncConfig['location']),calcFuncConfig['name'])

"""
manages all handlers and issues update commands
gets update lists and corresponding source codes for updates from message Router

"""
class handlerManager():
    def __init__(self, configDict):
        self.m_handlerConfig = configDict
        self.m_messageSubscriptions = {}
        self.m_end = False

        self.m_handlers = []
        self.m_scheduler = None

    def initAndStart(self, handlerData):
        self.m_scheduler = asyncScheduler()
        for h in self.m_handlers:
            
            self.m_scheduler.addTask(h.start())

    def loadHandlers(self, sharedData):
        print("---- Handler Manager Loading Blocks ----")

        for _, config in self.m_handlerConfig.items():
            h = self._loadHandler(config)
            h.m_handlerData = sharedData
            self.m_handlers.append(h)
        
        print("---- Handler Manager Done Loading ----")

    def _addSubscriptions(self, subscriptions, val):
        for subscription in subscriptions:
            subscription = subscription.lower()
            lst = self.m_messageSubscriptions.get(subscription, [])
            lst.append(val)
            self.m_messageSubscriptions[subscription] = lst

    def _loadHandler(self, config):
        name = config['name']
        subscriptions = config['subscriptions']
        calcFunc = _loadCalcFunc(config['calcFunc'])
        
        val = handler(name, calcFunc)
        self._addSubscriptions(subscriptions, val)
        return val

    def clear(self):
        self.m_handlers = None