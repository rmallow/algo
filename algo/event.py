from . import action as act
from . import feed as afd
from . import constants as con

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
            if feed.m_newCalcData[self.m_name].iloc[-1] == con.INSUF_DATA:
                start +=1
                self.m_parameters['first'] = True
                calcFuncVal = super().update(feed)
                feed.addToPartialCols({self.m_name : calcFuncVal})

            self.m_parameters['first'] = False
            for _ in range(start, len(feed.m_newCalcData.index)):
                calcFuncVal = super().update(feed)
                feed.addToPartialCols({self.m_name: calcFuncVal})
                
    def addINF(self, feed):
        """
        only put in as many insuf data as needed
        overall i feel like this function could use  good bit of reworking
        it feels like it currently handles things pretty inefficiently

        could probably add some flags so that we don't have to perform some inputs over and over
        """
        #this will check for the input cols and see if they have any insufficient data constants
        #it will find the last inf constant in any input col
        #insuf data at this point only applies to calc data, so skip a col if it's in data
        lastINFIndex = -1

        rangeIndexStart = self.m_period * -1
        
        for col in self.m_inputCols:
            if col not in feed.m_data.columns:
                #find the column and get just the parts we care about
                inputColDf = act.findCol(feed, col)
                rangeIndexEnd = len(inputColDf.index)
                inputColDf = inputColDf.iloc[rangeIndexStart:rangeIndexEnd]
                #kinda hacky but used isin and list instead of == to supress annoying numpy warning
                index = inputColDf.where(inputColDf.isin([con.INSUF_DATA])).last_valid_index()
                if index:
                    intIndex = inputColDf.index.get_loc(index)
                    if lastINFIndex < intIndex:
                        lastINFIndex = intIndex
                
                        #there won't be enough data to calculate so we just exit here to avoid unecessary computations
                        if lastINFIndex > feed.m_newCalcLength - self.m_period:
                            return [con.INSUF_DATA] * feed.m_newCalcLength
        
        #if we've made it here and lastINFIndex is not 0 then the starting point is just
        #period - 1 as INF was determined by the inputCols
        #if the columns can get other issues like errors and such filled in then this function will
        #need to be reworked
        INFListLength = 0
        if lastINFIndex > -1:
            #the actual math would be lastINFIndex + 1 + self.m_period - 1 but for obvious reasons i've slimmed that down
            #this is because of indexing stuff for lastIndex that it gets the add and period - 1 is stuff seen below
            INFListLength = lastINFIndex + self.m_period
        
        #check amount of data already calculated
        else:
            sub = 0
            if feed.m_calcData is not None and self.m_name in feed.m_calcData.columns:
                sub = len(feed.m_calcData.index)
            INFListLength = (self.m_period - 1 - sub) if (self.m_period - 1 - sub) > 0 else 0

        if INFListLength > feed.m_newCalcLength:
            INFListLength = feed.m_newCalcLength
        return [con.INSUF_DATA] * INFListLength

    def setupCols(self, feed):
       rowVals = self.addINF(feed)
       return {self.m_name: rowVals}