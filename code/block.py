from feed import feed
from actionPool import actionPool
from asyncScheduler import asyncScheduler
import pandas



class block():
    def __init__(self, actionList, feed, name ="defaultBlockName", subBlocks = [], top = False):
        #somehow options for the feed need to be read in here, can be implemented later, for now set manually
        self.m_feed = feed
        self.m_pool = actionPool(actionList, self.m_feed)
        self.m_subBlockList = subBlocks
        self.m_scheduler = None

        if top:
            self.m_scheduler = asyncScheduler(feed, self.m_pool)

    def start(self):
        self.m_scheduler.run()

    def clear(self):
        self.m_feed.clear()
        self.m_scheduler.stop()
