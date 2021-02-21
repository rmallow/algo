from .messageRouter import messageRouter
from .blockManager import blockManager
from .handlerManagerAsync import handlerManager
from .handlerData import handlerData

from .util import configLoader
from pathlib import Path
import os
import sys


def start():
    # init starter variables
    sharedData = handlerData()

    # init handler manager
    path = Path("/Users/rmallow/Documents/stonks/algo/config/testHandlerConfig.yml")
    configDict = configLoader.getConfigDictFromFile(path)
    mainHandlerManager = handlerManager(configDict)
    mainHandlerManager.loadHandlers(sharedData)

    # init message router
    mainMessageRouter = messageRouter(mainHandlerManager.m_messageSubscriptions, sharedData)

    # init block manager
    path = Path("/Users/rmallow/Documents/stonks/algo/config/demoBlockCryptoConfig.yml")
    configDict = configLoader.getConfigDictFromFile(path)
    mainBlockManager = blockManager(configDict, mainMessageRouter)
    mainBlockManager.loadBlocks()

    # this will set the current working directory from wherever to the directory this file is in
    # sys.path.append(os.path.dirname(os.path.abspath(sys.modules[__name__].__file__)))
    dirPath = os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))
    os.chdir(dirPath)

    mainBlockManager.start()
    mainMessageRouter.start()
    mainMessageRouter.join()
