import asyncio
import inspect
import logging


class asyncScheduler():
    def __init__(self, lockBool=False):
        self.m_loop = None
        self.m_tasks = []

    # this function is useful for multiprocessing
    # only pass in objects that have a start() that is awaitable
    def initAndStart(self, objects):
        self.init()
        try:
            for obj in objects:
                self.addTask(obj.start())
        except TypeError:
            self.addTask(objects.start())
        self.start()

    def init(self):
        self.m_loop = asyncio.new_event_loop()

    def start(self):
        if self.m_loop is None:
            self.m_loop = asyncio.new_event_loop()
        self.m_loop.run_until_complete(asyncio.wait(self.m_tasks))

    def end(self):
        self.m_loop.close()

    def addTask(self, func, name=None):
        if inspect.iscoroutine(func):
            self.m_tasks.append(self.m_loop.create_task(func, name=name))
        else:
            logging.warning("non coroutine function passed")

    def addTaskArgs(self, func, args, name=None):
        self.m_tasks.append(self.m_loop.create_task(func(args)))
