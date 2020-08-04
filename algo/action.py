col = 'col'
period = 'period'

def findCol(feed, col):
    if col in feed.m_data.columns:
        return feed.m_data[col]
    elif feed.m_calcData is not None and col in feed.m_calcData.columns:
        if col in feed.m_newCalcData.columns:
            return feed.m_calcData[col].append(feed.m_newCalcData[col])
        else:
            return feed.m_calcData[col]
    else:
        return None

#period refers to number of units, not time
class action():
    def __init__(self, actionType, period = 1, name = "defaultActionName", calcFunc = None, params = None):
        self.m_actionType = actionType
        self.m_period = period
        self.m_name = name
        self.m_calcFunc = calcFunc
        self.m_parameters = {**params, 'period':period}

    def update(self, feed):
        
        return self.m_calcFunc(feed, self.m_parameters)