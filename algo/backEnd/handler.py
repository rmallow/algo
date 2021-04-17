from .util import wrappers as wrap
from collections import OrderedDict

"""
handler class, takes message from message router and outputs
"""


class handler():
    def __init__(self, code, name, period, calcFunc, outputFunc, config, params=None, **kwargs):
        self.code = code
        self.name = name
        self.calcFunc = calcFunc
        self.outputFunc = outputFunc
        self.period = period
        self.handlerData = None
        self.personalData = OrderedDict()
        self.params = params
        self.config = config

    async def updatePriority(self, message):
        # this func will handle priority messages
        pass

    async def update(self, key):
        """
        @brief: called to update by message router to update handler
            when message subscription is hit

        @param: key - messageKey to update parameter on

        calls calcFunc and outputFunc if bool result of calcFunc is true
        parameters passed into funcs is:
            handlerData, params, personalData in that order

        TODO: handle passing functions based on arguement names,
            which means to update wrapper
        """
        # pass it to wrapper that handles correct number of args for function
        handlerData = self.handlerData.getPeriod(key, self.period)
        rawVal = wrap.adjustArgs(self.calcFunc, [handlerData, self.params, self.personalData])
        # then unpack the results, personalData return could be None
        # first result should always be boolResult
        boolResult, personalData = wrap.iterableReturnValue(rawVal, 2)

        # append personal data
        if personalData is not None:
            self.personalData[key] = personalData

        # after adjust personal data, call output function
        if boolResult:
            wrap.adjustArgs(self.outputFunc, [handlerData, self.params, self.personalData])
