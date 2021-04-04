from .block import block
from .event import event
from .trigger import trigger
from .feed import feed
from .dataSim import dataSim
from .dataStream import dataStream
from .dataFunc import dataFunc


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
        if 'constraint' in dataSourceConfig:
            dataSourceConfig |= dataSourceConfig['constaint']

        if dataSourceType == 'dataSim':
            return dataSim(**dataSourceConfig)
        elif dataSourceType == 'stream':
            return dataStream(**dataSourceConfig)
        elif dataSourceType == 'func':
            return dataFunc(**dataSourceConfig)

    def _loadActionList(self, actionListConfig):
        actionList = []
        for name, actionConfig in actionListConfig.items():
            action = None
            actionType = actionConfig['actionType']
            if actionType == 'trigger':
                action = trigger(**actionConfig)
            elif actionType == 'event':
                action = event(**actionConfig)
            actionList.append(action)
        return actionList

    def _loadFeed(self, feedConfig, dataFunc):
        return feed(dataFunc, **feedConfig)
