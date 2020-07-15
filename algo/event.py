from algo.action import action

class event(action):
    def __init__(self, period = 1, name = "defaultEventName", calcFunc = None, **kwargs):
        super().__init__("event", period=period, name=name, calcFunc=calcFunc, params = kwargs)

    def update(self, feed):
        cols = super().update(feed)
        return cols