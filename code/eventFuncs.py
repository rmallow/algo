from feed import feed

def testFunc(feed, **kwargs):
    return {"test4":12345, "periodTest": kwargs['period']}

def Average(lst): 
    return sum(lst) / len(lst) 

"""
Description: Returns the Simple Moving Average (SMA) using a passed in period
Output:
    sma: array
"""
def smaFunc(feed, **kwargs):
    neededLength = (kwargs['period']) - 1
    dataLength = len(feed.m_newData)
    recentData = []    
    array = []
    startingIndex = 0
    if((len(feed.m_data) < (neededLength + dataLength)) or dataLength == 0) and not(dataLength > neededLength + 1):
        return {"sma": 'insufData'}
    if(dataLength > neededLength + 1) and (len(feed.m_data) < (neededLength + dataLength)):
        recentData = feed.m_newData[:neededLength]
        startingIndex = neededLength 
        for n in range(neededLength):
            array.append('insufData')
    else:
        recentData = feed.m_data[: len(feed.m_data) - dataLength] [-neededLength:]
    recentClosesData = recentData['Close']
    recentCloses = []
    for n in recentClosesData:
        recentCloses.append(n)
    recentCloses.insert(0, 0)
    curCloses = feed.m_newData['Close']
    for n in curCloses[startingIndex:]:
        recentCloses = recentCloses[1:]
        recentCloses.append(n)
        avg = Average(recentCloses)
        array.append(avg)   
    return {"sma": array}