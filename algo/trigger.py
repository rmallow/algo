from algo.action import action

class trigger(action):
    def __init__(self, period=1, name = "defaultTriggerName", calcFunc = None, **kwargs):
        super().__init__("trigger", period=period, name=name, calcFunc=calcFunc, params = kwargs)

    def update(self, feed):
        messages = super().update(feed)
        return messages
