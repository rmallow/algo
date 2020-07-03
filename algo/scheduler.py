import sched
import time
import threading
from trigger import trigger

#NOW USING ASYNC SHECUDLER, THIS IS LEFT HERE JUST IN CASE
class scheduler():
    def __init__(self, actions, feed):
        self.m_sched = sched.scheduler(time.time, time.sleep)
        self.m_changeFeedActions = []
        self.m_lock = threading.Lock()
        self.m_continueBool = False
        self.m_feed = feed
        self.m_scheduleEventLocator = {}
        for action in actions:
            if action.m_onFeedChange is False:
                self._periodic(action)
            else:
                self.m_changeFeedActions.append(action) 
        self.m_changeFeedThread = threading.Thread(name="feedChangeActions",
            target = self._onFeedChangeAction, daemon=True)
        self.m_schedulerThread = threading.Thread(name="schedulerThread",
            target = self._schedulerRunNonBlocking, daemon=True)

    def _periodic(self, action):
        self.m_lock.acquire()
        event = self.m_sched.enter(action.m_timer, action.m_priority, self._periodic,
            (action,))
        self.m_lock.release()
        self.m_scheduleEventLocator[action.m_name] = event
        action.update(None, self.m_feed.getDataSince(action.m_lastTimestamp))

    def _onFeedChangeAction(self):
        while self.m_continueBool:
            self.m_feed.m_feedChangeEvent.wait(5)
            if self.m_feed.m_feedChangeEvent.is_set() and self.m_continueBool: 
            #check if e.is_set() in case of timeout
            #these are here to make sure it doesn't get stuck
                newData = self.m_feed.m_newData
                for action in self.m_changeFeedActions:
                    action.update(action.m_args, newData)
                self.m_feed.m_feedChangeEvent.clear()

    def _schedulerRunNonBlocking(self):
        while self.m_continueBool:
            self.m_sched.run(blocking=False)

    def run(self):
        self.m_continueBool = True
        self.m_changeFeedThread.start()
        self.m_schedulerThread.start()

    def addJob(self, action):
        self._periodic(action)

    def cancelJob(self, name):
        if name in self.m_scheduleEventLocator:
            self.m_sched.cancel(self.m_scheduleEventLocator[name])

    def end(self):
        self.m_continueBool = False
        self.m_changeFeedThread.join()
        self.m_schedulerThread.join()