import asyncio
import inspect
import logging

class asyncScheduler():
    def __init__(self, lockBool = False):
        self.m_loop = asyncio.new_event_loop()
        self.m_tasks = []

    def start(self):
        self.m_loop.run_until_complete(asyncio.wait(self.m_tasks))

    def end(self):
        self.m_loop.close()

    def addTask(self, func, name = None):
        if inspect.iscoroutinefunction(func):
            self.m_tasks.append(self.m_loop.create_task(func))
        else:
            logging.warning("non coroutine function passed")