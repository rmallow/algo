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
        self.m_updateQueue = mp.Queue()
        self.m_end = False

    def loadHandlers(self):
        print("---- Handler Manager Loading Blocks ----")
        for key, config in self.m_handlerConfig.items():
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

    def receive(self, message):
        self.m_updateQueue.put(message)
        
    def start(self):
        while not self.m_end:
            try:
                message = self.m_updateQueue.get(timeout=2)
            except queue.Empty:
                pass
            else:
                if message is not None:
                    #determine if message is a command
                    #only command that handler manager currently can get is abort, sent at end for cleanup
                    if message.m_type == msg.COMMAND_TYPE:
                        self.processCommand(message)
                    elif message.m_sourceCode is not None and message.m_message is not None:
                        for handler in message.m_message:
                            handler.update(message.m_sourceCode)

    def stop(self):
        self.m_end = True

    def processCommand(self, message):
        self.CMD_DICT.get(message.m_message,self.cmdNotFound)(self,message)

    def cmdNotFound(self, message):
        logging.warning("unrecognized command")
        logging.warning(str(message.m_message))

    def cmdAbort(self, message):
        self.m_end = True


    CMD_DICT = {
        msg.COMMAND_ABORT: cmdAbort
    }