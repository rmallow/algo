import time


def getStrTime(epochTime: float):    
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epochTime))