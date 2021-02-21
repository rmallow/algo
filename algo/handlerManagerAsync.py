from .handlerAsync import handler

import importlib
import logging


def _loadFunc(funcConfig):
    module = importlib.import_module(funcConfig['location'])
    if module is not None:
        if hasattr(module, funcConfig['name']):
            return getattr(module, funcConfig['name'])
        else:
            logging.warning("attr not found: " + funcConfig['name'] + "at module: " + funcConfig['location'])
    else:
        logging.warning("module not found: " + funcConfig['location'])
    return None


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

    def loadHandlers(self, sharedData):
        print("---- Handler Manager Loading Handlers ----")

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
        period = config['period']
        subscriptions = config['subscriptions']
        params = {}
        if 'params' in config:
            params = config['params']
        params['subscriptions'] = subscriptions
        calcFunc = _loadFunc(config['calcFunc'])
        outputFunc = _loadFunc(config['outputFunc'])

        val = handler(name, period, calcFunc, outputFunc, params=params)
        self._addSubscriptions(subscriptions, val)
        return val

    def clear(self):
        self.m_handlers = None
