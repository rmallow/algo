from .handlerAsync import handler


"""
manages all handlers and issues update commands
gets update lists and corresponding source codes for updates from message Router

"""


class handlerManager():
    def __init__(self, sharedData):
        self.sharedData = sharedData
        self.messageSubscriptions = {}

        self.handlers = {}

    # wrapper for UI to use
    def loadItem(self, configDict):
        self.loadHandlers(configDict)

    def loadHandlers(self, configDict):
        print("---- Handler Manager Loading Handlers ----")
        for code, config in configDict.items():
            if code in self.handlers:
                print("Handler code already exists: " + code)
            h = self._loadHandler(code, config)
            h.handlerData = self.sharedData
            self.handlers[code] = h

        print("---- Handler Manager Done Loading ----")

    def _addSubscriptions(self, subscriptions, val):
        for subscription in subscriptions:
            subscription = subscription.lower()
            lst = self.messageSubscriptions.get(subscription, [])
            lst.append(val)
            self.messageSubscriptions[subscription] = lst

    def _loadHandler(self, code, config):
        subscriptions = config['subscriptions']
        config['config'] = config
        if 'params' in config:
            config['params']['subscriptions'] = subscriptions

        val = handler(code, **config)
        self._addSubscriptions(subscriptions, val)
        return val

    def clear(self):
        self.handlers = None
