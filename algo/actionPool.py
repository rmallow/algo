from collections.abc import Iterable

import algo.action
import algo.message as msg
from algo.asyncScheduler import asyncScheduler
from algo.messageKey import messageKey

from requiremental import library
from requiremental import parser
from requiremental import libGroup

class actionPool():
    def __init__(self, actions, feed, messageRouter, code, libraries, parseSettings = None):
        self.m_feed = feed
        self.m_messageRouter = messageRouter
        self.m_code = code
        self.m_events = []
        self.m_triggers = []
        
        #set up requirementals
        """
        parse = parser.parser(settingsPath=parseSettings)

        self.m_library = library.library(parse)

        for libFile in libraries:
            self.m_library.loadFile(libFile)
        
        self.m_libGroup = libGroup.libGroup(library=self.m_libGroup)
        """
        #implement usage here, need to fix how requiremental works first


        for action in actions:
            self.addAction(action)

    def addAction(self, action):
        if action.m_actionType == "event":
            self.m_events.append(action)
        else:
            self.m_triggers.append(action)

    def doActions(self, newData):
        for event in self.m_events:
            #get pandas columns, append it then add that to calculated feed
            event.update(self.m_feed)
        
        self.m_feed.appendCalcData()

        if len(self.m_triggers) > 0:
            startKey = messageKey(self.m_code, self.m_feed.m_newData.index[0])
            startCmd = msg.message(msg.COMMAND_TYPE, msg.COMMAND_START, key = startKey)
            self.m_messageRouter.receive(startCmd)

            for trigger in self.m_triggers:
                messages = trigger.update(self.m_feed)
                if messages is not None:
                    #check if message iterable is received, otherwise check if one message
                    if isinstance(messages, Iterable):
                        for message in messages:
                            message.m_sourceCode = self.m_code
                            self.m_messageRouter.receive(message)
                    elif isinstance(messages, msg.message):
                        messages.m_sourceCode = self.m_code
                        self.m_messageRouter.receive(messages)
            
            endKey = messageKey(self.m_code,self.m_feed.m_newData.index[-1])
            endCmd = msg.message(msg.COMMAND_TYPE, msg.COMMAND_END, key = endKey)
            self.m_messageRouter.receive(endCmd)

    def sendAbortCommand(self):
        message = msg.message(msg.COMMAND_TYPE, msg.COMMAND_ABORT)
        self.m_messageRouter.receive(message)
        
            