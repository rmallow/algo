from . import action as act
from . import constants as con

from ..commonUtil import mpLogging


class event(act.action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, feed):
        # first set up col using util functions like INF and Not Found
        setupCols = self.setupCols(feed)
        feed.addNewCalcCols(setupCols)

        # do following for remaining amount of times until period
        #   call calcFunc to get calculated data
        #   add to feed, so future calcFunc calls can access it
        start = 0
        index = feed.newCalcData[self.name].last_valid_index()
        if index:
            start = feed.newCalcData.index.get_loc(index) + 1
        if start < len(feed.newCalcData.index):
            # checking whats the first calculated data needs to be fixed
            # first parameter can be used by functions to only do some computations on first attempt
            if feed.newCalcData[self.name].iloc[-1] == con.INSUF_DATA:
                start += 1
                self.parameters['first'] = True
                calcFuncVal = super().update(feed)
                feed.addToPartialCols({self.name: calcFuncVal})

            self.parameters['first'] = False
            for _ in range(start, len(feed.newCalcData.index)):
                calcFuncVal = super().update(feed)
                feed.addToPartialCols({self.name: calcFuncVal})

    def addINF(self, feed):
        """
        only put in as many insuf data as needed
        overall i feel like this function could use  good bit of reworking
        it feels like it currently handles things pretty inefficiently

        could probably add some flags so that we don't have to perform some inputs over and over

        this will check for the input cols and see if they have any insufficient data constants
        it will find the last inf constant in any input col
        insuf data at this point only applies to calc data, so skip a col if it's in data
        """
        lastINFIndex = -1

        rangeIndexStart = self.period * -1

        for col in self.inputCols:
            if col not in feed.data.columns:
                # find the column and get just the parts we care about
                inputColDf = act.findCol(feed, col)
                if inputColDf is None:
                    mpLogging.error("Adding inf but findCol found none",
                                    description=f"findCol called with col {col}")
                rangeIndexEnd = len(inputColDf.index)
                inputColDf = inputColDf.iloc[rangeIndexStart:rangeIndexEnd]
                # kinda hacky but used isin and list instead of == to supress annoying numpy warning
                index = inputColDf.where(inputColDf.isin([con.INSUF_DATA])).last_valid_index()
                if index:
                    intIndex = inputColDf.index.get_loc(index)
                    if lastINFIndex < intIndex:
                        lastINFIndex = intIndex

                        # there won't be enough data to calculate so we just exit here to avoid unecessary computations
                        if lastINFIndex > feed.newCalcLength - self.period:
                            return [con.INSUF_DATA] * feed.newCalcLength

        # if we've made it here and lastINFIndex is not 0 then the starting point is just
        # period - 1 as INF was determined by the inputCols
        # if the columns can get other issues like errors and such filled in then this function will
        # need to be reworked
        INFListLength = 0
        if lastINFIndex > -1:
            # the actual math would be lastINFIndex + 1 + self.period - 1
            # but for obvious reasons i've slimmed that down
            # this is because of indexing stuff for lastIndex that it gets the add and period - 1 is stuff seen below
            INFListLength = lastINFIndex + self.period

        # check amount of data already calculated
        else:
            sub = 0
            if feed.calcData is not None and self.name in feed.calcData.columns:
                sub = len(feed.calcData.index)
            INFListLength = (self.period - 1 - sub) if (self.period - 1 - sub) > 0 else 0

        if INFListLength > feed.newCalcLength:
            INFListLength = feed.newCalcLength
        return [con.INSUF_DATA] * INFListLength

    def setupCols(self, feed):
        rowVals = self.addINF(feed)
        return {self.name: rowVals}
