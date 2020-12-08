from . import action as act
from . import feed as afd

def addINF(feed, period, calcColName):
    sub = 0
    #only put in as many insuf data as needed
    if not(feed.m_calcData is None or calcColName not in feed.m_calcData.columns):
        sub = len(feed.m_calcData.index)
    INFListLength = (period - 1 - sub) if (period - 1 - sub) > 0 else 0

    if INFListLength > feed.m_newCalcLength:
        INFListLength = feed.m_newCalcLength
    return [afd.INSUF_DATA] * INFListLength
    

class event(act.action):
    def __init__(self, period=1, name="defaultEventName", calcFunc=None, params={}, inputCols = []):
        super().__init__("event", period=period, name=name, calcFunc=calcFunc, params = params, inputCols = inputCols)

    def update(self, feed):
        #first set up col using util functions like INF and Not Found
        setupCols = self.setupCols(feed)
        feed.addNewCalcCols(setupCols)
        
        #do following for remaining amount of times until period
        #   call calcFunc to get calculated data
        #   add to feed, so future calcFunc calls can access it
        start = 0
        index = feed.m_newCalcData[self.m_name].last_valid_index()
        if index:
            start = feed.m_newCalcData.index.get_loc(index) + 1
        if start < len(feed.m_newCalcData.index):
            #checking whats the first calculated data needs to be fixed
            if feed.m_newCalcData[self.m_name].iloc[-1] == afd.INSUF_DATA:
                start +=1
                self.m_parameters['first'] = True
                calcFuncVal = super().update(feed)
                feed.addToPartialCols({self.m_name : calcFuncVal})

            self.m_parameters['first'] = False
            for _ in range(start, len(feed.m_newCalcData.index)):
                calcFuncVal = super().update(feed)
                feed.addToPartialCols({self.m_name : calcFuncVal})

    def setupCols(self, feed):
       rowVals = addINF(feed, self.m_period, self.m_name)
       return {self.m_name: rowVals}