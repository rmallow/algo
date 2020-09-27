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
       rowVals = addINF(feed, self.m_period, self.m_name)
       return {self.m_name: rowVals}