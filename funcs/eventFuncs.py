import logging
import algo.action as act

"""
input for calcFuncs: dataset, params
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

def sma(dataSet, parameters=None):
    return dataSet.iloc[0].mean()

def change(dataSet, parameters=None):
    return dataSet.iloc[-1][0] - dataSet.iloc[0][0]
    
def up(dataSet, parameters=None):
    if dataSet.iloc[0][0] > 0:
        return dataSet.iloc[0][0]
    else:
        return 0

def down(dataSet, parameters=None):
    if dataSet.iloc[-1][0] < 0:
        return dataSet.iloc[-1][0]
    else:
        return 0