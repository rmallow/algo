from blockManager import blockManager
import configLoader

configDict = configLoader.getConfigDictFromFile("../config/testConfig.yml")

bM = blockManager(configDict)
bM.loadBlocks()

print(bM.m_blockList[0].m_pool.m_actions[1].m_childBlock.m_pool.m_actions[0].m_name)