from algo.handlerAsync import handler
import multiprocessing as mp
import importlib
import queue
import algo.message as msg
import logging
from algo.asyncScheduler import asyncScheduler

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
        self.m_scheduler = asyncScheduler()

    def loadHandlers(self):
        print("---- Handler Manager Loading Blocks ----")

        for _, config in self.m_handlerConfig.items():
            h = self._loadHandler(config)
            self.m_scheduler.addTask(h.start())
            self.m_handlers.append(h)
        
        print("---- Handler Manager Done Loading ----")

    def _addSubscriptions(self, subscriptions, val):
        for subscription in subscriptions:
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

    def end(self):
        self.m_handlers = None
        self.m_scheduler.end()
        self.m_scheduler = None

    def start(self):
        self.m_scheduler.start()