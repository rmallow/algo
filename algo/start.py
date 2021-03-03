from .backEnd.messageRouter import messageRouter
from .backEnd.blockManager import blockManager
from .backEnd.handlerManagerAsync import handlerManager
from .backEnd.handlerData import handlerData
from .controlBoard import controlBoard

from .backEnd.util import configLoader
from pathlib import Path
import os
import sys

from .ui.mainWindow import mainWindow
from PySide6 import QtWidgets


def start():
    if False:
        # init starter variables
        sharedData = handlerData()

        control = controlBoard()

        # init handler manager
        path = Path("/Users/rmallow/Documents/stonks/algo/config/testHandlerConfig.yml")
        configDict = configLoader.getConfigDictFromFile(path)
        mainHandlerManager = handlerManager(configDict)
        mainHandlerManager.loadHandlers(sharedData)

        # init message router
        mainMessageRouter = messageRouter(mainHandlerManager.m_messageSubscriptions, sharedData,
                                          control.m_MPManager.AioQueue())

        # init block manager
        path = Path("/Users/rmallow/Documents/stonks/algo/config/btcRSI.yml")
        configDict = configLoader.getConfigDictFromFile(path)
        mainBlockManager = blockManager(configDict, mainMessageRouter)
        mainBlockManager.loadBlocks()

        # this will set the current working directory from wherever to the directory this file is in
        # sys.path.append(os.path.dirname(os.path.abspath(sys.modules[__name__].__file__)))
        dirPath = os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))
        os.chdir(dirPath)

        control.runManagerAndRouter(mainBlockManager, mainMessageRouter)
        print("All process done, Closing")
    else:
        app = QtWidgets.QApplication([])

        mainWindow()

        sys.exit(app.exec_())
        
