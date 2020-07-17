import pandas as pd
import asyncio
import logging

#store data as necessary based on data source and desired period
#data in feed should be stored in programming language acessible containers
#feed is meant to be an inbetween from raw data to processed data

INSUF_DATA = 'insufData'
COL_NF = 'colNF'

class feed():

    def __init__(self, dataFunc, period = 1, continuous = False):
        self.m_getDataFunc = dataFunc
        #this period measures actual time, versus action period is just in units
        self.m_period = period	#if period is none, then ticks, otherwise period num in seconds
        self.m_continuous = continuous #if continuous is true, feed will update periods before full period time has elapsed

        self.m_lastTimestamp = None

        self.m_newData = None
        self.m_newCalcData = None
        self.m_data = None
        self.m_calcData = None
        
        self.m_end = False

    def updateHelper(self, rawData):
        if isinstance(rawData, pd.DataFrame):
            self.m_newData = rawData
        else:
            logging.warning("RAW DATA CONVERSION TO PANDAS NOT IMPLEMENTED YET")

        if self.m_newData is not None and len(self.m_newData.index) > 0:
            self.m_lastTimestamp = self.m_newData.index[-1]
            if self.m_data is None:
                self.m_data = self.m_newData
            else:
                self.m_data = self.m_data.append(self.m_newData)
        else:
            self.m_end = True

    async def asyncUpdate(self):
        rawData = await self.m_getDataFunc(self.m_lastTimestamp, self.m_period)
        if rawData is None:
            self.m_end = True
            return None
        self.updateHelper(rawData)
        self.m_newCalcData = pd.DataFrame(index=self.m_newData.index)
        return self.m_newData


    #not updated with most recent standards, do not use
    def update(self):
        rawData = self.m_getDataFunc(self.m_lastTimestamp, self.m_period)
        self.updateHelper(rawData)
        return self.m_newData

    def getDataSince(self, timestamp):
        if self.m_data is not None:
            return self.m_data.loc[timestamp:]
        return None

    def getNewData(self):
        return self.m_newData

    def appendCalcData(self):
        if self.m_calcData is None:
            self.m_calcData = self.m_newCalcData
        else:
            self.m_calcData = self.m_calcData.append(self.m_newCalcData, sort = True)

    def addNewCalcCols(self, cols):
        for key, value in cols.items():
            try:
                self.m_newCalcData[key] = value
            except ValueError as err:
                logging.warning("addNewCalcCols")
                logging.warning(err)