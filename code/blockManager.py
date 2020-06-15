import multiprocessing
from block import block
from event import event
from trigger import trigger
import pickle
from feed import feed
from dataSim import dataSim


def loadObj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def _loadBlockAndDataSource(blockConfig):
    dataSource = _loadDataSource(blockConfig['dataSource'])
    block = _loadBlock(blockConfig, dataSource.getData, top = True)
    return block, dataSource


def _loadBlock(blockConfig, dataFunc, top = False):
    name = blockConfig['name']
    feed = _loadFeed(blockConfig['feed'], dataFunc)
    subBlocks, actionList = _loadActionList(blockConfig['actionList'])
    return block(actionList, feed, name=name, subBlocks=subBlocks, top=top)

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
    subBlocks = []
    actionList = []
    for key, actionConfig in actionListConfig.items():
        action = None
        actionType = actionConfig['actionType']
        name = actionConfig['name']
        calcFunc = actionConfig['calcFunc']
        timer = actionConfig['timer']
        onFeedChange = actionConfig['onFeedChange']
        priority = actionConfig['priority']
        args = actionConfig['args']
        if actionType == 'trigger':
            #implement message router here
            action = trigger(name=name, calcFunc=calcFunc, timer=timer,
            onFeedChange=onFeedChange, args=args)
        elif actionType == 'event':
            action = event(name=name, calcFunc=calcFunc, timer=timer,
            onFeedChange=onFeedChange, args=args)
            subBlock = _loadBlock(actionConfig['block'], action.getData)
            subBlocks.append(subBlock)
            action.m_childBlock = subBlock
        actionList.append(action)
    return subBlocks, actionList

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
        #for key in self.m_groups:
        for key, config in self.m_assetBlockConfig.items():
            block, dataSource = _loadBlockAndDataSource(config)
            self.m_blockList.append(block)
            self.m_dataMangerList.append(dataSource)
            #get data manager of top level blcok and append to data managers list



