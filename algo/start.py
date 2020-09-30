from algo.messageRouter import messageRouter
from algo.blockManager import blockManager
from algo.handlerManager import handlerManager

import algo.util.configLoader as configLoader

import multiprocessing as mp
from pathlib import Path

def start():

    path = Path("/Users/rmallow/Documents/stonks/algo/config/testHandlerConfig.yml")
    configDict = configLoader.getConfigDictFromFile(path)
    hM = handlerManager(configDict)
    hM.loadHandlers()

    mR = messageRouter(hM)

    path = Path("/Users/rmallow/Documents/stonks/algo/config/testBlockConfig.yml")
    configDict = configLoader.getConfigDictFromFile(path)
    bM = blockManager(configDict, mR)
    bM.loadBlocks()

    p1 = mp.Process(target=hM.start)
    p1.start()

    p2 = mp.Process(target = mR.start)
    p2.start()

    p3 = mp.Process(target=bM.start)
    p3.start()

    p3.join()
    p1.join()
    p2.join()