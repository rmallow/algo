from .commonSettings import SETTINGS_FILE
from .commonGlobals import ITEM

from .backEnd import message as msg
from .backEnd.messageRouter import messageRouter
from .backEnd.blockManager import blockManager
from .backEnd.handlerManager import handlerManager
from .backEnd.handlerData import handlerData
from .backEnd.util import configLoader
from .backEnd.util.commandProcessor import commandProcessor

from multiprocess import Process, Manager
import aioprocessing
import os
import sys
import configparser
import time


class mainframe(commandProcessor):

    def __init__(self, uiQueue=None):
        super().__init__()
        self.processDict = {}
        self.routerProcess = None
        self.AioManager = aioprocessing.AioManager()
        self.MpManager = Manager()
        self.sharedData = handlerData()
        self.handlerManager = None
        self.blockManager = None
        self.mainframeQueue = self.MpManager.Queue()
        self.uiQueue = uiQueue

        # add commands for processor
        self.addCmdFunc(msg.CommandType.ADD_OUTPUT_VIEW, mainframe.addOutputView)

        # init handler manager
        # Load defaults
        self.loader = configLoader.configLoader(SETTINGS_FILE)

        config = configparser.ConfigParser()
        config.read(SETTINGS_FILE)
        blockConfigFile = ""
        handlerConfigFile = ""
        if 'Configs' in config:
            blockConfigFile = config.get('Configs', 'Block', fallback="")
            handlerConfigFile = config.get('Configs', 'Handler', fallback="")

        self.handlerManager = handlerManager(self.sharedData)
        self.loadHandlerConfig(handlerConfigFile)

        # init message router
        self.messageRouter = messageRouter(self.handlerManager.messageSubscriptions, self.sharedData,
                                           self.AioManager.AioQueue())

        # init block manager
        self.blockManager = blockManager(self.messageRouter)
        self.loadBlockConfig(blockConfigFile)

        for _, block in self.blockManager.blocks.items():
            block.blockQueue = self.MpManager.Queue()
            block.mainframeQueue = self.mainframeQueue

        # this will set the current working directory from wherever to the directory this file is in
        # sys.path.append(os.path.dirname(os.path.abspath(sys.modules[__name__].__file__)))
        dirPath = os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))
        os.chdir(dirPath)

    def start(self):
        while True:
            if self.mainframeQueue.empty():
                time.sleep(.3)
            else:
                message = self.mainframeQueue.get()
                if isinstance(message, msg.message):
                    if message.isCommand():
                        self.processCommand(message.content, message.details)
                    elif message.isUIUpdate():
                        if self.uiQueue is not None:
                            self.uiQueue.put(message)

    def addOutputView(self, command, details):
        if details[ITEM] in self.blockManager.blocks:
            block = self.blockManager.blocks[details[ITEM]]
            block.blockQueue.put(msg.message(msg.MessageType.COMMAND, command, details=details))

    def startRouter(self):
        self.routerProcess = Process(target=self.messageRouter.initAndStartLoop, name="Router")
        self.routerProcess.start()

    def runAll(self):
        if self.routerProcess is None:
            self.startRouter()

        for code, block in self.blockManager.blocks.items():
            if code not in self.processDict:
                self.startBlockProcess(code, block)
            else:
                print("Error Running Block: " + code)

    def runBlock(self, code):
        if self.routerProcess is None:
            self.startRouter()

        if code in self.blockManager.blocks and code not in self.processDict:
            block = self.blockManager.blocks[code]
            self.startBlockProcess(code, block)
        else:
            print("Error Running Block: " + code)

    def startBlockProcess(self, code, block):
        processName = "Block-" + str(code)
        blockProcess = Process(target=block.start, name=processName)
        self.processDict[code] = blockProcess
        blockProcess.start()

    def endAll(self):
        while self.processDict:
            for key, p in self.processDict.items():
                p.join(.5)
                if p.exitcode is not None:
                    del self.processDict[key]
        self.routerProcess.join()

    def endBlock(self, code, timeout=None):
        if code in self.processDict:
            if timeout:
                self.processDict[code].join(timeout)
            else:
                self.processDict[code].close()
            del self.processDict[code]

    def getBlocks(self):
        return self.blockManager.blocks

    def getHandlers(self):
        return self.handlerManager.handlers

    def loadBlockConfig(self, config):
        if config:
            configDict = self.loader.loadAndReplaceYamlFile(config)
            self.blockManager.loadBlocks(configDict)

    def loadHandlerConfig(self, config):
        if config:
            configDict = self.loader.loadAndReplaceYamlFile(config)
            self.handlerManager.loadHandlers(configDict)

    def loadConfigs(self, blockConfig, handlerConfig):
        self.loadBlockConfig(blockConfig)
        self.loadHandlerConfig(handlerConfig)
