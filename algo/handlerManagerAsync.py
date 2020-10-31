from algo.handler import handler
import multiprocessing as mp
import importlib
import queue
import algo.message as msg
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
        self.m_handlerList = []
        self.m_messageSubscriptions = {}
        self.m_end = False

    def loadHandlers(self):
        print("---- Handler Manager Loading Blocks ----")
        for _, config in self.m_handlerConfig.items():
            self.m_handlerList.append(self._loadHandler(config))
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