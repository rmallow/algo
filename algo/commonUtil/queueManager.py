# Note here we are using the dill version of the manger as we want dill queues
# multiprocess is dill wherhas multiprocessing is python built in
# Choosing SyncManger over BaseManager as this manager will also supply the blocks
# but those will not be acessible by outside connections
from multiprocess.managers import BaseManager


class QueueManager(BaseManager):
    pass


QueueManager.register("getMainframeQueue")
QueueManager.register("getUiQueue")
