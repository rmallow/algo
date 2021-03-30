from .commonSettings import SETTINGS_FILE

from .backEnd.messageRouter import messageRouter
from .backEnd.blockManager import blockManager
from .backEnd.handlerManagerAsync import handlerManager
from .backEnd.handlerData import handlerData
from .backEnd.util import configLoader

from multiprocess import Process, Manager
import aioprocessing
import os
import sys
import configparser
from PySide6 import QtCore, QtGui
import time


class mainframe(QtCore.QObject):
    dataChanged = QtCore.Signal()

    def __init__(self):
        super().__init__(None)
        self.m_processDict = {}
        self.m_routerProcess = None
        self.m_AioManager = aioprocessing.AioManager()
        self.m_MpManager = Manager()
        self.m_sharedData = handlerData()
        self.m_handlerManager = None
        self.m_blockManager = None
        self.m_mainframeQueue = self.m_MpManager.Queue()
        self.m_outputModel = QtGui.QStandardItemModel()

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

        self.m_handlerManager = handlerManager(self.m_sharedData)
        self.loadHandlerConfig(handlerConfigFile)

        # init message router
        self.m_messageRouter = messageRouter(self.m_handlerManager.m_messageSubscriptions, self.m_sharedData,
                                             self.m_AioManager.AioQueue())

        # init block manager
        self.m_blockManager = blockManager(self.m_messageRouter)
        self.loadBlockConfig(blockConfigFile)

        # this will set the current working directory from wherever to the directory this file is in
        # sys.path.append(os.path.dirname(os.path.abspath(sys.modules[__name__].__file__)))
        dirPath = os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))
        os.chdir(dirPath)

    def start(self):
        while True:
            if self.m_mainframeQueue.empty():
                time.sleep(.3)
            else:
                message = self.m_mainframeQueue.get()
                modelItem = QtGui.QStandardItem(message)
                self.m_outputModel.appendRow(modelItem)

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
        block.m_mainframeQueue = self.m_mainframeQueue
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

    def endBlock(self, code, timeout=None):
        if code in self.m_processDict:
            if timeout:
                self.m_processDict[code].join(timeout)
            else:
                self.m_processDict[code].close()
            del self.m_processDict[code]

    def getBlocks(self):
        return self.m_blockManager.m_blocks

    def getHandlers(self):
        return self.m_handlerManager.m_handlers

    def loadBlockConfig(self, config):
        if config:
            configDict = self.loader.loadAndReplaceYamlFile(config)
            self.m_blockManager.loadBlocks(configDict)

    def loadHandlerConfig(self, config):
        if config:
            configDict = self.loader.loadAndReplaceYamlFile(config)
            self.m_handlerManager.loadHandlers(configDict)

    def loadConfigs(self, blockConfig, handlerConfig):
        self.loadBlockConfig(blockConfig)
        self.loadHandlerConfig(handlerConfig)
