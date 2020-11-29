from algo.asyncScheduler import asyncScheduler
from algo.block import block
from algo.event import event
from algo.trigger import trigger
from algo.feed import feed
from algo.dataSim import dataSim

import requiremental

import pickle
import importlib
import logging
import multiprocessing


def _loadCalcFunc(calcFuncConfig):
    module = importlib.import_module(calcFuncConfig['location'])
    if module is not None:
        if hasattr(module, calcFuncConfig['name']):
            return getattr(module, calcFuncConfig['name'])
        else:
            logging.warning("attr not found: " + calcFuncConfig['name'] + "at module: " + calcFuncConfig['location'])
    else:
        logging.warning("module not found: " + calcFuncConfig['location'])
    return None

def loadObj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def _loadBlockAndDataSource(blockConfig, messageRouter):
    dataSource = _loadDataSource(blockConfig['dataSource'])
    name = blockConfig['name']
    feed = _loadFeed(blockConfig['feed'], dataSource.getDataFeed)
    actionList = _loadActionList(blockConfig['actionList'])
    libraries = blockConfig['libraries']
    blk = block(actionList, feed, messageRouter, libraries, name=name)
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
    for name, actionConfig in actionListConfig.items():
        action = None
        actionType = actionConfig['actionType']
        calcFunc = _loadCalcFunc(actionConfig['calcFunc'])
        period = actionConfig['period']
        params = {}
        inputCols = actionConfig['inputCols']
        if 'params' in actionConfig:
            params = actionConfig['params']
        if actionType == 'trigger':
            action = trigger(name=name, calcFunc=calcFunc, period=period, params = params, inputCols = inputCols)
        elif actionType == 'event':
            action = event(name=name, calcFunc=calcFunc, period = period, params = params, inputCols = inputCols)
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
        for _, config in self.m_assetBlockConfig.items():
            block, dataSource = _loadBlockAndDataSource(config, self.m_messageRouter)
            self.m_blockList.append(block)
            self.m_dataMangerList.append(dataSource)
        print("---- Block Manager Done Loading ----")

    def start(self):
        for block in self.m_blockList:
            block.start()
            print(block.m_feed.m_data)
            print(block.m_feed.m_calcData)