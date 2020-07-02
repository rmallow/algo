from handler import handler
import multiprocessing as mp
import importlib
import queue

def _loadCalcFunc(calcFuncConfig):
    return getattr(importlib.import_module(calcFuncConfig['location']),calcFuncConfig['name'])



class handlerManager():
    def __init__(self, configDict, messageRouter):
        self.m_handlerConfig = configDict
        self.m_handlerList = []
        self.m_messageRouter = messageRouter
        self.m_updateQueue = mp.Queue()
        self.m_end = False

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
        return handler(name, calcFunc)

    def receive(self, message):
        self.m_updateQueue.put(message)
        
    def start(self):
        while not self.m_end:
            try:
                val = self.m_updateQueue.get(timeout=2)
            except queue.Empty:
                pass
            else:
                code = val[0]
                lst = val[1]
                if code is not None and lst is not None:
                   for handler in lst:
                       handler.update(code)