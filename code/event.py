from action import action

class event(action):
    def __init__(self, childBlock = None, timer = 1, name = "defaultEventName", priority = 5, args = (),
        onFeedChange = False, calcFunc = None):
        super().__init__(timer=timer, name=name, priority=priority,
        args=args, onFeedChange=onFeedChange, calcFunc=calcFunc)

        self.m_calculatedNewData = None
        self.m_childBlock = childBlock	#probably should be a block?

    def update(self, args, newData):
        super().update(newData)
    
    def getData(self, timestamp, period):
        #should probably implement period control eventually
        #can't see why timestamp can't be ignored
        return self.m_calculatedNewData