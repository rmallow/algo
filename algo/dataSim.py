from .dataBase import dataBase
from .dataConstants import DataTypeEnum

from .util import csvDataUtil as cdu
from .util import requestUtil as ru

import sys
import os


#use this to load data and send to feeds for backtesting/simulation

class dataSim(dataBase):
    def __init__(self, key, dataType, indexName = None, period = None, columnFilter = None):
        super().__init__(key, dataType, indexName, period, columnFilter)

        self.m_data = None
        self.m_newDay = False
        self.loadData()
    
    def loadData(self):
        if self.m_dataType == DataTypeEnum.CSV:
            keyData = cdu.loadSingleCSV(self.m_key, index="Local time")
            self.m_key = keyData[0]
            self.m_data = keyData[1]
        elif self.m_dataType == DataTypeEnum.DIR:
            keyData = cdu.combineDirCSV(self.m_key, index="Local time")
            self.m_key = keyData[0]
            self.m_data = keyData[1]
        elif self.m_dataType == DataTypeEnum.URL:
            self.m_data = ru.getPandasFromUrl(self.m_key, indexName = self.m_indexName, columnFilter=self.m_columnFilter)

        self.m_data.columns = [x.lower() for x in self.m_data.columns]

    def getData(self, timestamp, period, getType):
        if getType == "stock":
            return self.getDataStock(timestamp, period)
        elif getType == "continuous":
            return self.getDataContinuous(timestamp,period)


    def getDataStock(self, timestamp, period):
        #timestamp should be last data recieved, start of data will be next timestamp
        afterData = None
        if timestamp is None:
            timestamp = self.m_data.index[0]
        else:
            timestamp = self.m_data.loc[timestamp:].index[1]
        afterData = self.m_data.loc[timestamp:]
        #for now we are just going to assume data is correctly indexed
        timesAfter = afterData.index
        timesAfter.tz_convert('US/Central')
        timestamp.tz_convert('US/Central')
        index = -1
        startIndex = -1
        for idx, time in enumerate(timesAfter):
            index = idx
            #times are in CST, might wanna make sure timestamp is CST just in case
            if time.hour < 8 or (time.hour == 8 and time.minute < 31):
                startIndex += 1
                timestamp = time
                continue
            elif time.day != timestamp.day or time.hour >= 15:
                self.m_newDay = True
                break
            elif (time - timestamp).total_seconds() >= period:
                break

        if index == -1:
            #no new values to return
            return None
        else:
            startIndex = 0 if startIndex < 0 else startIndex
            #combine data to fit period
            return afterData[startIndex:index]

    """
    this func is pretty much a copy of getdata stock without checking for new day or market hours
    at some point some of the code can be clumped together but for now this works
    """
    def getDataContinuous(self, timestamp, period):
        afterData = None
        if timestamp is None:
            timestamp = self.m_data.index[0]
        else:
            timestamp = self.m_data.loc[timestamp:].index[1]
        afterData = self.m_data.loc[timestamp:]

        timesAfter = afterData.index
        index = -1
        for idx, time in enumerate(timesAfter):
            index = idx
            if (time - timestamp).total_seconds() >= period:
                break

        if index == -1:
            #no new values to return
            return None
        else:
            return afterData[:index]

    def getDataFeed(self, timestamp, period):
        return self.getData(timestamp, period, "stock")