from multiprocess import Process
from pathos.multiprocessing import ProcessingPool as Pool
import aioprocessing
import time


class controlBoard():
    def __init__(self, manager=None):
        if manager is not None:
            self.m_MPManager = manager
        else:
            self.m_MPManager = aioprocessing.AioManager()

    def runManagerAndRouter(self, manager, router):
        processCount = len(manager.m_blockList)
        pool = Pool(nodes=processCount)

        pRouter = Process(target=router.initAndStartLoop, name="Router")
        pRouter.start()

        results = pool.amap(lambda block: block.start(), manager.m_blockList)
        while not results.ready():
            time.sleep(5)

        if results.ready():
            for result in results.get():
                print(result[0])
                print(result[1])

        pool.close()
        pRouter.join()
