import algo.action
import algo.message as msg
from algo.asyncScheduler import asyncScheduler
from algo.messageKey import messageKey

from requiremental import library
from requiremental import parser
from requiremental import libGroup

from collections.abc import Iterable


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

            #tell message router tha triggers are going to start sending messages
            startKey = messageKey(self.m_code, self.m_feed.m_newData.index[0])
            startCmd = msg.message(msg.COMMAND_TYPE, msg.COMMAND_START, key = startKey)
            self.m_messageRouter.receive(startCmd)



            #
            #   various checks done on how to handle values/messages returned from trigger funcs
            #
            sentMessageList = []
            for trigger in self.m_triggers:
                rawTriggerValue = trigger.update(self.m_feed)
                if rawTriggerValue is not None:
                    if isinstance(rawTriggerValue, str):
                        sentMessage = msg.message(msg.NORMAL_TYPE, rawTriggerValue, key = startKey, name = trigger.m_name)
                        sentMessageList.append(sentMessage)
                    elif isinstance(rawTriggerValue, Iterable):
                        for rawMessage in rawTriggerValue:
                            sentMessage = None
                            if isinstance(rawMessage, msg.message):
                                #rawMessage are already message class messages
                                sentMessage = rawMessage  
                                if sentMessage.m_key is None:
                                    sentMessage.m_key = startKey
                                sentMessage.m_name = trigger.m_name  
                            else:
                                sentMessage = msg.message(msg.NORMAL_TYPE, rawMessage, key = startKey, name = trigger.m_name)
                            
                            if sentMessage.isPriority():    
                                self.m_messageRouter.receive(sentMessage)
                            else:
                                sentMessageList.append(sentMessage)
                    elif isinstance(rawTriggerValue, msg.message):
                        #rawMessage are already message class messages
                        sentMessage = rawTriggerValue
                        if sentMessage.m_key is None:
                                    sentMessage.m_key = startKey
                        sentMessage.m_name = trigger.m_name  
                        if sentMessage.isPriority():    
                            self.m_messageRouter.receive(sentMessage)
                        else:
                            sentMessageList.append(sentMessage)
            
            #send all the non priority messages
            self.m_messageRouter.receive(sentMessageList)
            #
            #   End of trigger func updating and sending to message router
            #
            

            #tell message router tha triggers are going to done sending messages
            #handlers should now be told to process this block of messages
            

            endKey = messageKey(self.m_code,self.m_feed.m_newData.index[-1])
            endCmd = msg.message(msg.COMMAND_TYPE, msg.COMMAND_END, key = endKey)
            self.m_messageRouter.receive(endCmd)

    def sendAbortCommand(self):
        message = msg.message(msg.COMMAND_TYPE, msg.COMMAND_ABORT)
        self.m_messageRouter.receive(message)
        
            