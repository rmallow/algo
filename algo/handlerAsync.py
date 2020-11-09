import algo.message
from algo.commandProcessor import commandProcessor

import aioprocessing
import asyncio
from queue import Empty
import multiprocessing as mp


"""
handler class, takes message from message router and outputs


"""
class handler(commandProcessor):
    def __init__(self, name, calcFunc):
        self.m_name = name
        self.m_calcFunc = calcFunc
        self.m_data = None

        self.m_buffer = {}
        self.m_messageQueue = aioprocessing.AioQueue()
        self.m_commandQueue = aioprocessing.AioQueue()

    def receiveMessage(self, message):
        # pylint: disable=no-member
        self.m_messageQueue.put(message)

    def coroReceiveMessage(self, message):
        # pylint: disable=no-member
        self.m_messageQueue.coro_put(message)

    def receiveCommand(self, command):
        # pylint: disable=no-member
        self.m_commandQueue.put(command)

    def coroReceiveCommand(self, command):
        # pylint: disable=no-member
        self.m_commandQueue.coro_put(command)

    def cmdEnd(self, command):
        pass

    async def start(self):
        while True:
            try:
                # pylint: disable=no-member
                command = await self.m_commandQueue.coro_get(timeout=.25)
            except Empty:
                pass
            else:
                if command is None:
                    continue
                else:
                    self.processCommand(command)
