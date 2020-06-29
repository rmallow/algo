from blockManager import blockManager
import configLoader

configDict = configLoader.getConfigDictFromFile("../config/testBlockConfig.yml")

bM = blockManager(configDict)
bM.loadBlocks()

bM.start()