from action import action

class trigger(action):
    def __init__(self, timer = 1, name = "defaultTriggerName", priority = 5, args = (), 
        onFeedChange = False, calcFunc = None):
        super().__init__(timer=timer, name=name, priority=priority,
        args=args, onFeedChange=onFeedChange, calcFunc=calcFunc)

        self.m_messageRouter = None

    def update(self, args, newData):
        super().update(newData)