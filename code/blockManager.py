import multiprocessing
from block import block
from event import event
from trigger import trigger
import pickle
from feed import feed
from dataSim import dataSim
import importlib

def _loadCalcFunc(calcFuncConfig):
    return getattr(importlib.import_module(calcFuncConfig['location']),calcFuncConfig['name'])

def loadObj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def _loadBlockAndDataSource(blockConfig):
    dataSource = _loadDataSource(blockConfig['dataSource'])
    block = _loadBlock(blockConfig, dataSource.getData)
    return block, dataSource


def _loadBlock(blockConfig, dataFunc, top = False):
    name = blockConfig['name']
    feed = _loadFeed(blockConfig['feed'], dataFunc)
    actionList = _loadActionList(blockConfig['actionList'])
    return block(actionList, feed, name=name)

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
    def __init__(self,configDict):
        self.m_assetBlockConfig = configDict
        self.m_blockList = []
        self.m_dataMangerList = []

    def loadBlocks(self):
        print("---- Block Manager Loading Blocks ----")
        for key, config in self.m_assetBlockConfig.items():
            block, dataSource = _loadBlockAndDataSource(config)
            self.m_blockList.append(block)
            self.m_dataMangerList.append(dataSource)
        print("---- Block Manager Done Loading ----")


