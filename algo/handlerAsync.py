import algo.message

import asyncio

"""
handler class, takes message from message router and outputs
"""
class handler():
    def __init__(self, name, calcFunc):
        self.m_name = name
        self.m_calcFunc = calcFunc
        self.m_personalData = None
        self.m_handlerData = None
        
    async def updatePriority(self, message):
        #this func will handle priority messages that this handler is subscribed to
        pass

    async def update(self, key):
        #pass in key to look in handler date for what it needs
        pass
