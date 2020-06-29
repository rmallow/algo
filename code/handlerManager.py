from handler import handler
import importlib

def _loadCalcFunc(calcFuncConfig):
    return getattr(importlib.import_module(calcFuncConfig['location']),calcFuncConfig['name'])



class handlerManager():
    def __init__(self, configDict, messageRouter):
        self.m_handlerConfig = configDict
        self.m_handlerList = []
        self.m_messageRouter = messageRouter

    def loadHandlers(self):
        print("---- Handler Manager Loading Blocks ----")
        for key, config in self.m_handler.items():
            self.m_handlerList.append(self._loadHandler(config))
        print("---- Handler Manager Done Loading ----")

    def _loadHandler(self, config):
        name = config['name']
        subscriptions = config['subscriptions']
        calcFunc = _loadCalcFunc(config['calcFunc'])
        
        self.m_messageRouter.addSubscriptions(subscriptions)
        return handler(name,calcFunc)