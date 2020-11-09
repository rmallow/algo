from algo.messageRouter import messageRouter
from algo.blockManager import blockManager
from algo.handlerManagerAsync import handlerManager

import algo.util.configLoader as configLoader

import multiprocessing as mp
from pathlib import Path

def start():

    path = Path("/Users/rmallow/Documents/stonks/algo/config/testHandlerConfig.yml")
    configDict = configLoader.getConfigDictFromFile(path)
    hM = handlerManager(configDict)
    hM.loadHandlers()

    mR = messageRouter(hM.m_messageSubscriptions)

    path = Path("/Users/rmallow/Documents/stonks/algo/config/testBlockConfig.yml")
    configDict = configLoader.getConfigDictFromFile(path)
    bM = blockManager(configDict, mR)
    bM.loadBlocks()