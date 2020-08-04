import algo.feed as afd
import logging
import algo.action as act



"""
input for calcFuncs: dataset, params
do as much error handling as possibble outside of calcFunc
"""



"""
Description: Returns the Simple Moving Average (SMA)
Output:
    sma-${col}: array
"""

def sma(feed, params):
    col = params.get(act.col, 'Close')
    calcColName = 'sma-' + col
    s = findCol(feed, col)
    period = params[act.period]
    array = afd.COL_NF
    if s is not None:
        array = afd.INSUF_DATA
        if s.size >= period:
            array = []
            dataPoint = None
            #if an sma needs to be calculated for first time
            if feed.m_calcData is None or calcColName not in feed.m_calcData.columns or feed.m_calcData[calcColName].iloc[len(feed.m_calcData.index) - 1] == afd.INSUF_DATA:
                array = addINF(feed, period, calcColName)
                dataPoint = s[0:period].sum() / period
                index = period
                array.append(dataPoint)
            else:
                index = len(feed.m_calcData.index) - 1
                dataPoint = feed.m_calcData[calcColName].iloc[index]

            #calculate the rest of the sma's
            for num in range(1, s.size - index):
                dataPoint = (dataPoint * period - s[index + num - period] + s[index + num]) / period
                array.append(dataPoint)
                
    return {calcColName: array}

"""
Description: Returns the Exponential Moving Average (EMA)
Output:
    ema-${col}: array
"""
def ema(feed, params):
    
    return {"ema": 0}

def change(feed, params):
    col = params.get(act.col, 'Close')
    calcColName = 'change-' + col
    s = findCol(feed, col)
    array = afd.COL_NF
    if s is not None:
        array = afd.INSUF_DATA
        if s.size > 1:
            array = []
            if feed.m_calcData is None or calcColName not in feed.m_calcData.columns:
                array.append(afd.INSUF_DATA)
                start = 1
            else:
                start = s.size - len(feed.m_newCalcData.index)
            for num in range(start, s.size):
                array.append(s[num] - s[num - 1])
                
    return {calcColName: array}

def up(feed, params):
    col = params.get(act.col, 'Close')
    calcColName = 'up-' + col
    s = findCol(feed, col)
    array = afd.COL_NF
    if s is not None:
        array = []
        for data in s:
            #TODO: check if data is number
            if data > 0.0:
                array.append(data)
            else:
                array.append(0.0)

    return {calcColName, array}

def down(feed, params):
    col = params.get(act.col, 'Close')
    calcColName = 'down-' + col
    s = findCol(feed, col)
    array = afd.COL_NF
    if s is not None:
        array = []
        for data in s:
            #TODO: check if data is number
            if data < 0.0:
                array.append(data)
            else:
                array.append(0.0)

    return {calcColName, array}