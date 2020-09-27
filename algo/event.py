import algo.action as act
import algo.feed as afd

def addINF(feed, period, calcColName):
    sub = 0
    #only put in as many insuf data as needed
    if not(feed.m_calcData is None or calcColName not in feed.m_calcData.columns):
        sub = len(feed.m_calcData.index)
    INFListLength = (period - 1 - sub) if (period - 1 - sub) > 0 else 0

    return [afd.INSUF_DATA] * INFListLength
    

class event(act.action):
    def __init__(self, period=1, name="defaultEventName", calcFunc=None, params={}):
        super().__init__("event", period=period, name=name, calcFunc=calcFunc, params = params)

    def update(self, feed):
        feed.addPartialCols(self.setupCols(feed))
        cols = super().update(feed)
        feed.addNewCalcCols(cols)

    def setupCols(self, feed):
       rowVals = addINF(feed, self.m_period, )


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