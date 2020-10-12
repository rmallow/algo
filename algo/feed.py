import pandas as pd
import asyncio
import logging
import numpy as np
import collections

def safeLength(value):
    """
    use this for values that could be an unknown type
    """
    if isinstance(value, collections.Iterable) and not isinstance(value, str):
        return len(value)
    else:
        return 1

def setFrameColRange(frame, col, start, values):
    stop = start + safeLength(values) - 1
    if start == stop:
        stop += 1
    frame.iloc[start:stop, frame.columns.get_loc(col)] = values 



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
        
        self.m_newCalcLength = 0
        self.m_end = False

    def updateHelper(self, rawData):
        if isinstance(rawData, pd.DataFrame):
            self.m_newData = rawData
        else:
            logging.warning("RAW DATA CONVERSION TO PANDAS NOT IMPLEMENTED YET")

        if self.m_newData is not None and len(self.m_newData.index) > 0:
            self.m_lastTimestamp = self.m_newData.index[-1]
            if self.m_data is None:
                #first time setup here
                #self.m_newData.columns = [x.lower() for x in self.m_newData.columns]
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
        self.m_newCalcLength = len(self.m_newCalcData.index)  #conveience
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
            self.m_calcData = self.m_calcData.append(self.m_newCalcData, sort=True)
        #this is necessary otherwise indexing gets weird for triggers
        self.m_newCalcData = None

    def addNewCalcCols(self, cols):
        for key, value in cols.items():
            if key in self.m_newCalcData:
                self.addToPartialCols({key: value})
            else:
                self.safeAddCol(key, value)
    
    def safeAddCol(self, key, value):
        #safeValue = makeDataSafeList(value)
        if safeLength(value) == len(self.m_newCalcData.index):
            try:
                self.m_newCalcData[key.lower()] = value
            except ValueError as err:
                logging.warning("attempted to add col of same length")
                logging.warning(err)
        else:
            self.m_newCalcData[key.lower()] = np.nan
            self.addToPartialCols({key:value})

    def addToPartialCols(self, cols):
        """
        used for adding partially either new or to an existing column
        """
        for key, value in cols.items():
            if key:
                start = 0
                if key in self.m_newCalcData:
                    #start and stop are for correctly indexing gow to add to col
                    index = self.m_newCalcData[key].last_valid_index()
                    if index:
                        start = self.m_newCalcData.index.get_loc(index) + 1
                #if key not in there, will add from 0
                setFrameColRange(self.m_newCalcData, key, start, value)
            else:
                logging.warning("key not exist addToPartialCols")
