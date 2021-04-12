def testFunc1():
    pass


def testFunc2(handlerData):
    print(handlerData)


# need to refactor this once names is done
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

    return (True, "buy")


def alwaysTrue():
    return (True, "buy")


def printOutput():
    print("I'm an output function")


def buyCodePrint(_, _2, personal):
    key = list(personal.keys())[-1]
    print("Buy " + key.sourceCode + " at " + str(key.time))


def sellCodePrint(_, _2, personal):
    key = list(personal.keys())[-1]
    print("Sell " + key.sourceCode + " at " + str(key.time))


def countPersonal(_, _2, personal):
    print("Length of personal: " + str(len(personal)))
