import asyncio
import logging
"""
class asyncScheduler():
    def __init__(self, actions, feed):
        self.m_feed = feed
        self.m_actions = actions
        self.m_task = None

    #called during sub updating
    def updateOnce(self):
        newData = self.m_feed.update()
        for action in self.m_actions:
            action.update((),newData)
            if hasattr(action, 'm_childBlock') and action.m_childBlock is not None:
                action.m_childBlock.subUpdate()

    #called during top level data source updating
    async def asyncUpdate(self):
        while True:
            if self.m_feed.m_end is True:
                self.stop()
            newData = await self.m_feed.asyncUpdate()
            for action in self.m_actions:
                action.update((), newData)
                if hasattr(action, 'm_childBlock') and action.m_childBlock is not None:
                    action.m_childBlock.subUpdate()


    def run(self):
        loop = asyncio.get_event_loop()
        self.m_task = loop.create_task(self.asyncUpdate())

        try:
	        loop.run_until_complete(self.m_task)   
        except asyncio.CancelledError:
	        pass

    def stop(self):
        self.m_task.cancel()


"""

class asyncScheduler():
    def __init__(self, feed, pool):
        self.m_feed = feed
        self.m_actionPool = pool
        self.m_task = None

    async def asyncUpdate(self):
        while True:
            if self.m_feed.m_end:
                self.stop()
                break
            newData = await self.m_feed.asyncUpdate()
            self.m_actionPool.doActions(newData)

    def run(self):
        loop = asyncio.get_event_loop()
        self.m_task = loop.create_task(self.asyncUpdate())

        try:
            loop.run_until_complete(self.m_task)   
        except asyncio.CancelledError:
            if not self.m_feed.m_end:
                logging.warning("async cncelled error")

    def stop(self):
        self.m_task.cancel()

            