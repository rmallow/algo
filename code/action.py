import feed

class action():
    def __init__(self, actionType, period = 1, name = "defaultActionName", calcFunc = None, cols = cols):
        self.m_actionType = actionType
        self.m_period = period
        self.m_name = name
        self.m_cols = cols
        self.m_calcFunc = calcFunc

    def update(self, feed, **kwargs):
        return self.m_calcFunc(feed, period = self.m_period, cols = self.m_cols,)