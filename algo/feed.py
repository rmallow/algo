from . import constants as con

import pandas as pd
import asyncio
import logging
import numpy as np
import collections
import time

def safeLength(value):
    """
    use this for values that could be an unknown type
    """
    if isinstance(value, collections.Iterable) and not isinstance(value, str):
        return len(value)
    else:
        return 1

def setFrameColRange(frame, col, start, values):
    #REMOVED -1 FROM THE END OF THIS??
    stop = start + safeLength(values)
    if start == stop:
        stop += 1
    try:
        frame.iloc[start:stop, frame.columns.get_loc(col)] = values
    except ValueError:
        pass



"""
data storage and processing system for block
contains multiple containers for data and calc data along with new/all
appending functions for pandas data
"""
class feed():

    def __init__(self, dataFunc, period = 1, continuous = False):
        self.m_getDataFunc = dataFunc
        #this period measures actual time, versus action period is just in units
        self.m_period = period	#if period is none, then ticks, otherwise period num in seconds
        self.m_continuous = continuous  #if continuous is true, feed will update periods before full period time has elapsed
        
        
        """
        Various data holders for feed:
            data - holds all data in current cycle
            newData - holds all data in current update
            calcData - holds all calculated data in current cycle
            newCalcData - holds all currently calculated date in current update
                - this dataframe is added to continuously during action pool event updates
                    therefore might not have all columns/rows as the other dataframes
        """

        self.m_data = None
        self.m_newData = None
        self.m_calcData = None
        self.m_newCalcData = None
        
        self.m_newCalcLength = 0
        self.m_end = False

        self.m_startTime = time.time()

    def updateHelper(self, rawData):
        self.m_newData = rawData
        if self.m_newData is not None and len(self.m_newData.index) > 0:
            if self.m_data is None:
                #first time setup here
                #self.m_newData.columns = [x.lower() for x in self.m_newData.columns]
                self.m_data = self.m_newData
            else:
                self.m_data = self.m_data.append(self.m_newData)
        else:
            self.m_end = True
        self.m_newCalcData = pd.DataFrame(index=self.m_newData.index)
        self.m_newCalcLength = len(self.m_newCalcData.index)  #conveience

    def update(self):
        rawData = self.m_getDataFunc(self.m_period)
        if rawData is None:
            self.m_end = True
            return None
        elif not isinstance(rawData, pd.DataFrame):
            if rawData == con.OUTSIDE_CONSTRAINT:
                #return constant to block, block will clear feed and tell Message Router to clear
                return rawData
            else:
                logging.warning("Unexpected type passed to feed from data input, returning None")
                return None
        #rawData could still be empty
        self.updateHelper(rawData)
        return self.m_newData

    def getDataSince(self, index):
        if self.m_data is not None:
            return self.m_data.loc[index:]
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
            if safeLength(value) > 0:
                self.addToPartialCols({key:value})

    def addToPartialCols(self, cols):
        """
        used for adding partially 
        either new or to an existing column
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

    def clear(self):
        self.m_data = None
        self.m_newData = None
        self.m_calcData = None
        self.m_newCalcData = None