from . import constants as con

from ..commonUtil import mpLogging
from ..commonGlobals import FEED_GROUP

import pandas as pd
from numpy import nan as numpyNan
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
    # REMOVED -1 FROM THE END OF THIS??
    stop = start + safeLength(values)
    if start == stop:
        stop += 1
    try:
        frame.iloc[start:stop, frame.columns.get_loc(col)] = values
    except ValueError:
        pass


class feed():
    """
    data storage and processing system for block
    contains multiple containers for data and calc data along with new/all
    appending functions for pandas data
    """
    def __init__(self, dataFunc, period=1, continuous=False, unique=False):
        self.getDataFunc = dataFunc
        # this period measures actual time, versus action period is just in units
        self.period = period	 # if period is none, then ticks, otherwise period num in seconds
        self.continuous = continuous
        # if continuous is true, feed will update periods before full period time has elapsed

        self.unique = unique

        """
        Data holders for feed:
            data - holds all data in current cycle
            newData - holds all data in current update
            calcData - holds all calculated data in current cycle
            newCalcData - holds all currently calculated date in current update
                - this dataframe is added to continuously during action pool event updates
                    therefore might not have all columns/rows as the other dataframes
        """

        self.data = None
        self.newData = None
        self.calcData = None
        self.newCalcData = None

        self.newCalcLength = 0
        self.end = False

        self.startTime = time.time()

    def updateHelper(self, rawData):
        if self.unique and 'uid' in rawData.columns:
            self.dropNonUniques(rawData)

        if len(rawData.index) <= 0:
            # Tell block there was nothing unique, need to call update again
            return con.DataSourceReturnEnum.NO_DATA

        self.newData = rawData
        if self.newData is not None:
            if self.data is None:
                # first time setup here
                # self.newData.columns = [x.lower() for x in self.newData.columns]
                self.data = self.newData
            else:
                self.data = self.data.append(self.newData)
        else:
            self.end = True
        self.newCalcData = pd.DataFrame(index=self.newData.index)
        self.newCalcLength = len(self.newCalcData.index)  # conveience
        return None

    def update(self):
        rawData = self.getDataFunc(self.period)
        if rawData is None:
            mpLogging.warning("Data source returned none", group=FEED_GROUP,
                              description="Don't return none, use END_DATA to end.")
            return rawData
        elif not isinstance(rawData, pd.DataFrame):
            if (rawData == con.DataSourceReturnEnum.OUTSIDE_CONSTRAINT or rawData == con.DataSourceReturnEnum.NO_DATA
               or rawData == con.DataSourceReturnEnum.END_DATA):
                # return constant to block, block will clear feed and tell Message Router to clear
                return rawData
            else:
                mpLogging.warning("Unexpected type passed to feed from data input, returning None", group=FEED_GROUP)
                return None
        # rawData could still be empty
        helperReturn = self.updateHelper(rawData)
        if helperReturn and helperReturn == con.DataSourceReturnEnum.NO_DATA:
            self.update()

        return self.newData

    def getDataSince(self, index):
        if self.data is not None:
            return self.data.loc[index:]
        return None

    def getNewData(self):
        return self.newData

    def appendCalcData(self):
        if self.calcData is None:
            self.calcData = self.newCalcData
        else:
            self.calcData = self.calcData.append(self.newCalcData, sort=True)
        # this is necessary otherwise indexing gets weird for triggers
        self.newCalcData = None

    def addNewCalcCols(self, cols):
        for key, value in cols.items():
            if key in self.newCalcData:
                self.addToPartialCols({key: value})
            else:
                self.safeAddCol(key, value)

    def safeAddCol(self, key, value):
        if safeLength(value) == len(self.newCalcData.index):
            try:
                self.newCalcData[key.lower()] = value
            except ValueError:
                mpLogging.warning("Attempted to add col of same length", group=FEED_GROUP,
                                  description=f"Key: {key}")
        else:
            self.newCalcData[key.lower()] = numpyNan
            if safeLength(value) > 0:
                self.addToPartialCols({key: value})

    def addToPartialCols(self, cols):
        """
        used for adding partially
        either new or to an existing column
        """
        for key, value in cols.items():
            if key:
                start = 0
                if key in self.newCalcData:
                    # start and stop are for correctly indexing gow to add to col
                    index = self.newCalcData[key].last_valid_index()
                    if index:
                        start = self.newCalcData.index.get_loc(index) + 1
                # if key not in there, will add from 0
                setFrameColRange(self.newCalcData, key, start, value)
            else:
                mpLogging.warning("Key doesn't exist in AddToPartialCols", group=FEED_GROUP,
                                  description=f"Key: {key}")

    def clear(self):
        self.data = None
        self.newData = None
        self.calcData = None
        self.newCalcData = None

    def dropNonUniques(self, df):
        """
        Pass in a datafarame to compare against self.data to drop non unique values
        """
        if self.data is not None and df is not None:
            try:
                self.data.uid
                df.uid
            except AttributeError:
                mpLogging.printTraceback("uid not found", group=FEED_GROUP,
                                         description="uid not found in either self.data or newData of \
                                            feed but unique set to true")
            else:
                dropList = []
                for index in df.index:
                    uid1 = df.loc[index].uid
                    feedUidSeries = self.data.uid
                    if uid1 in feedUidSeries.unique():
                        dropList.append(index)

                df.drop(dropList, inplace=True)
