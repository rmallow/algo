import feed

class action():
    def __init__(self, timer = 1, name = "defaultActionName", priority = 5, args = (), 
        onFeedChange = False, calcFunc = None):
        self.m_timer = timer
        self.m_name = name
        self.m_priority = priority
        self.m_args = args  #might remove args
        self.m_onFeedChange = onFeedChange

        #member variables not assigned at initiation
        self.m_data = None        #might not be necessary
        self.m_lastTimestamp = None
        self.m_calcFunc = calcFunc

    def update(self, newData):
        x=2