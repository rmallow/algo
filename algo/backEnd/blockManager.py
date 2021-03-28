from .block import block
from .event import event
from .trigger import trigger
from .feed import feed
from .dataSim import dataSim
from .dataStream import dataStream
from .dataFunc import dataFunc

from .util import configLoader


class blockManager():
    def __init__(self, messageRouter):
        self.m_blocks = {}
        self.m_dataMangerList = {}
        self.m_messageRouter = messageRouter

    def loadItem(self, configDict):
        self.loadBlocks(configDict)

    def loadBlocks(self, configDict):
        print("---- Block Manager Loading Blocks ----")
        for code, config in configDict.items():
            print("Loading Block with code: " + code)
            self._loadBlockAndDataSource(config, code)
        print("---- Block Manager Done Loading ----")

    def _loadBlockAndDataSource(self, blockConfig, code):
        dataSource = self._loadDataSource(blockConfig['dataSource'])
        name = blockConfig['name']
        feed = self._loadFeed(blockConfig['feed'], dataSource.getData)
        actionList = self._loadActionList(blockConfig['actionList'])
        libraries = blockConfig['libraries']
        blk = block(actionList, feed, self.m_messageRouter, libraries, blockConfig, name=name, code=code)
        self.m_blocks[code] = blk
        self.m_dataMangerList[code] = dataSource

    def _loadDataSource(self, dataSourceConfig):
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
        elif dataSourceType == 'func':
            func = configLoader.loadFunc(dataSourceConfig['func'])
            params = dataSourceConfig['params']
            return dataFunc(key, dataType, func, params, index, period, colFilter, lowerConstraint, upperConstraint, dayFirst)

    def _loadActionList(self, actionListConfig):
        actionList = []
        for name, actionConfig in actionListConfig.items():
            action = None
            actionType = actionConfig['actionType']
            calcFunc = configLoader.loadFunc(actionConfig['calcFunc'])
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

    def _loadFeed(self, feedConfig, dataFunc):
        period = feedConfig['period']
        continuous = feedConfig['continuous']
        return feed(dataFunc, period=period, continuous=continuous)
