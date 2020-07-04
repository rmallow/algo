import multiprocessing
from algo.block import block
from algo.event import event
from algo.trigger import trigger
import pickle
from algo.feed import feed
from algo.dataSim import dataSim
import importlib

def _loadCalcFunc(calcFuncConfig):
    return getattr(importlib.import_module(calcFuncConfig['location']),calcFuncConfig['name'])

def loadObj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def _loadBlockAndDataSource(blockConfig, messageRouter):
    dataSource = _loadDataSource(blockConfig['dataSource'])
    name = blockConfig['name']
    feed = _loadFeed(blockConfig['feed'], dataSource.asyncGetData)
    actionList = _loadActionList(blockConfig['actionList'])
    blk = block(actionList, feed, messageRouter, name=name)
    return blk, dataSource

def _loadDataSource(dataSourceConfig):
    dataSourceType = dataSourceConfig['type']
    key = dataSourceConfig['key']
    if dataSourceType == 'dataSim':
        fileType = dataSourceConfig['fileType']
        return dataSim(key, fileType)
    elif dataSourceType == 'stream':
        #return stream(key)
        return None #change after implementing stream

def _loadActionList(actionListConfig):
    actionList = []
    for key, actionConfig in actionListConfig.items():
        action = None
        actionType = actionConfig['actionType']
        name = actionConfig['name']
        calcFunc = _loadCalcFunc(actionConfig['calcFunc'])
        period = actionConfig['period']
        if actionType == 'trigger':
            #implement message router here
            action = trigger(name=name, calcFunc=calcFunc, period=period)
        elif actionType == 'event':
            action = event(name=name, calcFunc=calcFunc, period = period)
        actionList.append(action)
    return actionList

def _loadFeed(feedConfig, dataFunc):
    period = feedConfig['period']
    continuous = feedConfig['continuous']
    return feed(dataFunc, period=period, continuous=continuous)

class blockManager():
    def __init__(self,configDict, messageRouter):
        self.m_assetBlockConfig = configDict
        self.m_blockList = []
        self.m_dataMangerList = []
        self.m_messageRouter = messageRouter

    def loadBlocks(self):
        print("---- Block Manager Loading Blocks ----")
        for key, config in self.m_assetBlockConfig.items():
            block, dataSource = _loadBlockAndDataSource(config, self.m_messageRouter)
            self.m_blockList.append(block)
            self.m_dataMangerList.append(dataSource)
        print("---- Block Manager Done Loading ----")

    def start(self):
        for block in self.m_blockList:
            block.start()