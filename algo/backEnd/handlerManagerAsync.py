from .handlerAsync import handler

from .util import configLoader


"""
manages all handlers and issues update commands
gets update lists and corresponding source codes for updates from message Router

"""


class handlerManager():
    def __init__(self, sharedData):
        self.m_sharedData = sharedData
        self.m_messageSubscriptions = {}

        self.m_handlers = []

    def loadHandlers(self, configDict):
        print("---- Handler Manager Loading Handlers ----")
        for code, config in configDict.items():
            h = self._loadHandler(code, config)
            h.m_handlerData = self.m_sharedData
            self.m_handlers.append(h)

        print("---- Handler Manager Done Loading ----")

    def _addSubscriptions(self, subscriptions, val):
        for subscription in subscriptions:
            subscription = subscription.lower()
            lst = self.m_messageSubscriptions.get(subscription, [])
            lst.append(val)
            self.m_messageSubscriptions[subscription] = lst

    def _loadHandler(self, code, config):
        name = config['name']
        period = config['period']
        subscriptions = config['subscriptions']
        params = {}
        if 'params' in config:
            params = config['params']
        params['subscriptions'] = subscriptions
        calcFunc = configLoader.loadFunc(config['calcFunc'])
        outputFunc = configLoader.loadFunc(config['outputFunc'])

        val = handler(code, name, period, calcFunc, outputFunc, params=params)
        self._addSubscriptions(subscriptions, val)
        return val

    def clear(self):
        self.m_handlers = None
