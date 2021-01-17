from .messageRouter import messageRouter
from .blockManager import blockManager
from .handlerManagerAsync import handlerManager
from .handlerData import handlerData
from .asyncScheduler import asyncScheduler

import algo.util.configLoader as configLoader

import multiprocessing as mp
from multiprocessing.managers import BaseManager
from pathlib import Path

def start():
    #init starter variables
    sharedData = handlerData()

    #init handler manager
    path = Path("/Users/rmallow/Documents/stonks/algo/config/testHandlerConfig.yml")
    configDict = configLoader.getConfigDictFromFile(path)
    mainHandlerManager = handlerManager(configDict)
    mainHandlerManager.loadHandlers(sharedData)

    #init message router
    mainMessageRouter = messageRouter(mainHandlerManager.m_messageSubscriptions, sharedData)

    #init block manager
    path = Path("/Users/rmallow/Documents/stonks/algo/config/demoBlockReqConfig.yml")
    configDict = configLoader.getConfigDictFromFile(path)
    mainBlockManager = blockManager(configDict, mainMessageRouter)
    mainBlockManager.loadBlocks()

    #get objects that have start() awaitables for scheduler

    pRouter = mp.Process(target = mainMessageRouter.initAndStart)
    pMainBlockManager = mp.Process(target = mainBlockManager.start)

    pRouter.start()
    pMainBlockManager.start()
    
    pRouter.join()
    pMainBlockManager.join()