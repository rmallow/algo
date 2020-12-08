from .dataConstants import DataTypeEnum

from .util import requestUtil as ru

import logging

class dataStream():
    def __init__(self, key, dataType, url):
        self.m_key = key
        try:
            self.m_dataType = DataTypeEnum[dataType]
        except ValueError:
            logging.warning("Failed setting data type")
            logging.warning(self.m_dataType)
        self.m_url = url

    def getData(self, timestamp, period):
        if self.m_dataType == DataTypeEnum.HISTORICAL:
            pass
        elif self.m_dataType == DataTypeEnum.REAL_TIME:
            return self.getDataReal(timestamp, period)

    def getDataReal(self, timestamp, period):
        return ru.getPandasFromUrl(self.m_url)

    def getDataFeed(self, timestamp, period):
        return self.getData(timestamp, period)