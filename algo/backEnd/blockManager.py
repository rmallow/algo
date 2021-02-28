from .block import block
from .event import event
from .trigger import trigger
from .feed import feed
from .dataSim import dataSim
from .dataStream import dataStream

import importlib
import logging


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


def _loadBlockAndDataSource(blockConfig, messageRouter, code):
    dataSource = _loadDataSource(blockConfig['dataSource'])
    name = blockConfig['name']
    feed = _loadFeed(blockConfig['feed'], dataSource.getData)
    actionList = _loadActionList(blockConfig['actionList'])
    libraries = blockConfig['libraries']
    blk = block(actionList, feed, messageRouter, libraries, name=name, code=code)
    return blk, dataSource


def _loadDataSource(dataSourceConfig):
    dataSourceType = dataSourceConfig['type']
    key = dataSourceConfig['key']
    dataType = dataSourceConfig['dataType']
    index = dataSourceConfig['index']
    colFilter = dataSourceConfig['columnFilter']
    period = dataSourceConfig['period']
    upperConstraint = None
    lowerConstraint = None
    if 'constraint' in dataSourceConfig:
        lowerConstraint = dataSourceConfig['constraint']['lower']
        upperConstraint = dataSourceConfig['constraint']['upper']
    dayFirst = dataSourceConfig['dayFirst']
    if dataSourceType == 'dataSim':
        return dataSim(key, dataType, index, period, colFilter, lowerConstraint, upperConstraint, dayFirst)
    elif dataSourceType == 'stream':
        return dataStream(key, dataType, index, period, colFilter, lowerConstraint, upperConstraint, dayFirst)


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
            action = trigger(name=name, calcFunc=calcFunc, period=period, params=params, inputCols=inputCols)
        elif actionType == 'event':
            action = event(name=name, calcFunc=calcFunc, period=period, params=params, inputCols=inputCols)
        actionList.append(action)
    return actionList


def _loadFeed(feedConfig, dataFunc):
    period = feedConfig['period']
    continuous = feedConfig['continuous']
    return feed(dataFunc, period=period, continuous=continuous)


class blockManager():
    def __init__(self, configDict, messageRouter, blockOnJoin=True):
        self.m_assetBlockConfig = configDict
        self.m_blockList = []
        self.m_dataMangerList = []
        self.m_messageRouter = messageRouter
        self.m_results = None
        self.m_pool = None
        self.m_blockOnJoin = blockOnJoin
        self.m_startTime = None

    def loadBlocks(self):
        print("---- Block Manager Loading Blocks ----")
        for code, config in self.m_assetBlockConfig.items():
            block, dataSource = _loadBlockAndDataSource(config, self.m_messageRouter, code)
            self.m_blockList.append(block)
            self.m_dataMangerList.append(dataSource)
        print("---- Block Manager Done Loading ----")
