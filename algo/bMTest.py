from blockManager import blockManager
from handlerManager import handlerManager
import configLoader

"""
have to add messageRouter to block manager creation before uncommeting


configDict = configLoader.getConfigDictFromFile("../config/testBlockConfig.yml")

bM = blockManager(configDict)
bM.loadBlocks()
"""

configDict = configLoader.getConfigDictFromFile("../config/testHandlerConfig.yml")
hM = handlerManager(configDict)
hM.loadHandlers()

print(hM.m_messageSubscriptions)

for handler in hM.m_handlerList:
    print(handler.m_name)