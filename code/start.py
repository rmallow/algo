from messageRouter import messageRouter
from blockManager import blockManager
from handlerManager import handlerManager

import configLoader

import multiprocessing as mp

def main():
    
    configDict = configLoader.getConfigDictFromFile("../config/testHandlerConfig.yml")
    hM = handlerManager(configDict)
    hM.loadHandlers()

    mR = messageRouter(hM)

    configDict = configLoader.getConfigDictFromFile("../config/testBlockConfig.yml")
    bM = blockManager(configDict, messageRouter)
    bM.loadBlocks()

if __name__ == '__main__':
    main()