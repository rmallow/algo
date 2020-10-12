import algo.feed as afd
import logging
import algo.action as act

import random



"""
input for calcFuncs: dataset, params
do as much error handling as possibble outside of calcFunc
"""



"""
Description: Returns the Simple Moving Average (SMA)
Output:
    sma-${col}: array
"""

def testFunc(dataSet, parameters = None):
    return dataSet['close'].iloc[0] + 1

def ema(dataSet, parameters=None):
    smooth = act.getParameter(parameters, 'smooth', 2)
    period = len(dataSet.index)
    ema = None
    for _, row in dataSet.iterrows():
        if ema is None:
            ema = row[0]
        else:
            ema = row[0] * (smooth / (period + 1)) + ema * (1 - (smooth / (period + 1)))
    return ema
