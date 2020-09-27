import asyncio
import logging
import traceback
import sys
from . import algoLogging

class asyncScheduler():
    def __init__(self, feed, pool):
        self.m_feed = feed
        self.m_actionPool = pool
        self.m_task = None

    async def asyncUpdate(self):
        while True:
            newData = await self.m_feed.asyncUpdate()
            if self.m_feed.m_end:
                self.m_actionPool.sendAbortCommand()
                self.stop()
                break
            elif newData is not None:
                self.m_actionPool.doActions(newData)

    def run(self):
        loop = asyncio.get_event_loop()
        self.m_task = loop.create_task(self.asyncUpdate())

        try:
            loop.run_until_complete(self.m_task)   
        except asyncio.CancelledError:
            if not self.m_feed.m_end:
                logging.warning("async cancelled error")
        except Exception as e:
            logging.warning(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            warning = traceback.extract_tb(exc_traceback)
            logging.warning(algoLogging.formatTraceback(warning))

            
            


    def stop(self):
        self.m_task.cancel()

            