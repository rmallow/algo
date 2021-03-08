from .commonSettings import SETTINGS_FILE

from .backEnd.messageRouter import messageRouter
from .backEnd.blockManager import blockManager
from .backEnd.handlerManagerAsync import handlerManager
from .backEnd.handlerData import handlerData
from .backEnd.util import configLoader

from multiprocess import Process
from pathos.multiprocessing import ProcessingPool as Pool
import aioprocessing
import time
import os
import sys
import configparser


class mainframe():
    def __init__(self, manager=None):
        if manager is not None:
            self.m_MPManager = manager
        else:
            self.m_MPManager = aioprocessing.AioManager()

        sharedData = handlerData()

        # init handler manager
        # Load defaults
        config = configparser.ConfigParser()
        config.read(SETTINGS_FILE)
        blockConfigFile = ""
        handlerConfigFile = ""
        if 'Configs' in config:
            blockConfigFile = config.get('Configs', 'Block', fallback="")
            handlerConfigFile = config.get('Configs', 'Handler', fallback="")

        self.m_handlerManager = handlerManager(sharedData)
        if handlerConfigFile:
            configDict = configLoader.getConfigDictFromFile(handlerConfigFile)
            self.m_handlerManager.loadHandlers(configDict)

        # init message router
        self.m_messageRouter = messageRouter(self.m_handlerManager.m_messageSubscriptions, sharedData,
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

    def runManagerAndRouter(self):
        processCount = len(self.m_blockManager.m_blocks)
        pool = Pool(nodes=processCount)

        pRouter = Process(target=self.m_messageRouter.initAndStartLoop, name="Router")
        pRouter.start()

        results = pool.amap(lambda block: block.start(), self.m_blockManager.m_blocks)
        while not results.ready():
            time.sleep(2)

        if results.ready():
            for result in results.get():
                print(result[0])
                print(result[1])

        pool.close()
        pRouter.join()
