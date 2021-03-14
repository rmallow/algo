from .commonSettings import SETTINGS_FILE

from .backEnd.messageRouter import messageRouter
from .backEnd.blockManager import blockManager
from .backEnd.handlerManagerAsync import handlerManager
from .backEnd.handlerData import handlerData
from .backEnd.util import configLoader

from multiprocess import Process
import aioprocessing
import os
import sys
import configparser


class mainframe():
    def __init__(self):

        self.m_processDict = {}
        self.m_routerProcess = None
        self.m_MPManager = aioprocessing.AioManager()
        self.m_sharedData = handlerData()
        self.m_handlerManager = None
        self.m_blockManager = None

        # init handler manager
        # Load defaults
        config = configparser.ConfigParser()
        config.read(SETTINGS_FILE)
        blockConfigFile = ""
        handlerConfigFile = ""
        if 'Configs' in config:
            blockConfigFile = config.get('Configs', 'Block', fallback="")
            handlerConfigFile = config.get('Configs', 'Handler', fallback="")

        self.m_handlerManager = handlerManager(self.m_sharedData)
        if handlerConfigFile:
            configDict = configLoader.getConfigDictFromFile(handlerConfigFile)
            self.m_handlerManager.loadHandlers(configDict)

        # init message router
        self.m_messageRouter = messageRouter(self.m_handlerManager.m_messageSubscriptions, self.m_sharedData,
                                             self.m_MPManager.AioQueue())

        # init block manager
        self.m_blockManager = blockManager(self.m_messageRouter)
        if blockConfigFile:
            configDict = configLoader.getConfigDictFromFile(blockConfigFile)
            self.m_blockManager.loadBlocks(configDict)

        # this will set the current working directory from wherever to the directory this file is in
        # sys.path.append(os.path.dirname(os.path.abspath(sys.modules[__name__].__file__)))
        dirPath = os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))
        os.chdir(dirPath)

    def startRouter(self):
        self.m_routerProcess = Process(target=self.m_messageRouter.initAndStartLoop, name="Router")
        self.m_routerProcess.start()

    def runAll(self):
        if self.m_routerProcess is None:
            self.startRouter()

        for code, block in self.m_blockManager.m_blocks.items():
            if code not in self.m_processDict:
                self.startBlockProcess(code, block)
            else:
                print("Error Running Block: " + code)

    def runBlock(self, code):
        if self.m_routerProcess is None:
            self.startRouter()

        if code in self.m_blockManager.m_blocks and code not in self.m_processDict:
            block = self.m_blockManager.m_blocks[code]
            self.startBlockProcess(code, block)
        else:
            print("Error Running Block: " + code)

    def startBlockProcess(self, code, block):
        processName = "Block-" + str(code)
        blockProcess = Process(target=block.start, name=processName)
        self.m_processDict[code] = blockProcess
        blockProcess.start()

    def endAll(self):
        while self.m_processDict:
            for key, p in self.m_processDict.items():
                p.join(.5)
                if p.exitcode is not None:
                    del self.m_processDict[key]
        self.m_routerProcess.join()

    def getBlocks(self):
        return self.m_blockManager.m_blocks

    def getHandlers(self):
        return self.m_handlerManager.m_handlers
