import algo.feed as afd

def testFunc(feed, **kwargs):
    return {"test4":12345, "periodTest": kwargs['period']}

def average(lst): 
    return sum(lst) / len(lst) 

"""
Description: Returns the Simple Moving Average (SMA) using a passed in period
Output:
    sma: array
"""

def sma(feed, **kwargs):
    colValue = ""
    try:
        kwargs['col']
    except:
        colValue = 'Close'
    else:
        colValue = kwargs['col']

    neededLength = (kwargs['period']) - 1
    dataLength = len(feed.m_newData)
    recentData = []    
    array = []
    startingIndex = 0
    #if the old data is too small and the new data is too small
    if((len(feed.m_data) < (neededLength + dataLength)) or dataLength == 0) and not(dataLength > neededLength + 1):
        return {"sma": afd.INSUF_DATA}
    #if the old data is too small but the new data is large enough
    if(dataLength > neededLength + 1) and (len(feed.m_data) < (neededLength + dataLength)):
        recentData = feed.m_newData[:neededLength]
        startingIndex = neededLength 
        for n in range(neededLength):
            array.append(afd.INSUF_DATA)
    else:
        recentData = feed.m_data[: len(feed.m_data) - dataLength] [-neededLength:]
    recentColsData = recentData[colValue]
    recentCols = []
    for n in recentColsData:
        recentCols.append(n)
    recentCols.insert(0, 0)
    curCols = feed.m_newData[colValue]
    for n in curCols[startingIndex:]:
        recentCols = recentCols[1:]
        recentCols.append(n)
        avg = average(recentCols)
        array.append(avg)   
    return {"sma": array}

"""
Description: Returns the Exponential Moving Average (EMA) using a passed in period
Output:
    ema: array
"""
def ema(feed, **kwargs):
    colValue = ""
    try:
        kwargs['col']
    except:
        colValue = 'Close'
    else:
        colValue = kwargs['col']  

    smoothingFactor = 0
    try:
        kwargs['smooth']
    except:
        smoothingFactor = 2
    else:
        smoothingFactor = kwargs['smooth']

    neededLength = (kwargs['period'])
    multiplier = (smoothingFactor/(neededLength+1))
    dataLength = len(feed.m_newData)
    fullLength = len(feed.m_data)
    recentData = []    
    array = []
    startingIndex = 0
    #if the old data is too small and the new data is too small
    if((len(feed.m_data) < (neededLength + dataLength)) or dataLength == 0) and not(dataLength > neededLength + 1):
        return {"ema": afd.INSUF_DATA}
    #if the old data is too small but the new data is large enough
    if(dataLength > neededLength + 1) and (len(feed.m_data) < (neededLength + dataLength)):
        recentData = feed.m_newData[:neededLength]
        startingIndex = neededLength 
        for n in range(neededLength):
            array.append(afd.INSUF_DATA)
    else:
        recentData = feed.m_data[: len(feed.m_data) - dataLength] [-neededLength:]
    recentColsData = recentData[colValue]
    recentCols = []
    for n in recentColsData:
        recentCols.append(n)
    prevema = ""
    try:        
        len(feed.m_calcData)
    except:
        prevema = afd.INSUF_DATA
    else:
        lastCalcdata = feed.m_calcData.iloc[-1:]
        prevema = lastCalcdata['ema'].item()
    if(prevema == afd.INSUF_DATA):
        prevema = average(recentCols)
    curCols = feed.m_newData[colValue]
    for n in curCols[startingIndex:]:
        ema = (n * multiplier) + (prevema * (1-multiplier))
        prevema = ema
        array.append(ema)
    return {"ema": array}