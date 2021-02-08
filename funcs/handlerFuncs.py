def testFunc1():
    pass

def testFunc2(handlerData):
    print(handlerData)

def containsOneOfEach(handlerData, params):
    checkList = []
    if params is not None and 'subscriptions' in params and len(params['subscriptions']) > 0:
        checkList = [False] * len(params['subscriptions'])
    else:
        return False
    for k in handlerData:
        for x in range(0, len(checkList)):
            if not checkList[x]:
                if params['subscriptions'][x] in handlerData[k]:
                    checkList[x] = True

    for check in checkList:
        if not check:
            return False

    return True
            
        

def printOutput():
    print("I'm an output function")