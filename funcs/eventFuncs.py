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