import logging

_extraKwargs = ['group', 'source', 'description']

_mpKwarg = '_mpKwarg'


def adjustKwarg(kwargDict):
    if 'extra' not in kwargDict:
        kwargDict['extra'] = {}
    kwargDict['extra'][_mpKwarg] = True
    kwargDict['exc_info'] = True


def handleRecordData(recordData):
    if recordData is not None:
        try:
            record = logging.makeLogRecord(recordData)

            logger = logging.getLogger(record.name)
            if logger.isEnabledFor(record.levelno):
                logger.handle(record)
        except Exception:
            logging.exception("Error in log handler")


class MPLogger(logging.Logger):
    log_queue = None
    mpKey: str = None

    def isEnabledFor(self, level):
        return True

    def handle(self, record):
        try:
            record._mpKwarg
        except AttributeError:
            pass
        else:
            if record._mpKwarg:
                ei = record.exc_info
                if ei:
                    # to get traceback text into record.exc_text
                    logging._defaultFormatter.format(record)
                    record.exc_info = None  # not needed any more
                d = dict(record.__dict__)
                d['msg'] = record.getMessage()
                d['args'] = None
                d['mpKey'] = self.mpKey
                self.log_queue.put(d)
                return

        # if attribute not present or is present and is false
        super().handle(record)

    def log(self, level, msg, *args, **kwargs):
        for kwarg in _extraKwargs:
            if kwarg in kwargs:
                if 'extra' not in kwargs:
                    kwargs['extra'] = {}
                kwargs['extra'][kwarg] = kwargs[kwarg]
                del kwargs[kwarg]
        # stacklevel is used in logging.findCaller, it is the number of frames on the stack
        # to go back, in our case it needs to go four back to find where the mpLogging was caleld
        super().log(level, msg, *args, **kwargs, stacklevel=4)

    def mpCritical(self, msg, *args, **kwargs):
        adjustKwarg(kwargs)
        self.log(logging.CRITICAL, msg, *args, **kwargs)

    def mpError(self, msg, *args, **kwargs):
        adjustKwarg(kwargs)
        self.log(logging.ERROR, msg, *args, **kwargs)

    def mpWarning(self, msg, *args, **kwargs):
        adjustKwarg(kwargs)
        self.log(logging.WARNING, msg, *args, **kwargs)

    def mpInfo(self, msg, *args, **kwargs):
        adjustKwarg(kwargs)
        self.log(logging.INFO, msg, *args, **kwargs)

    def mpDebug(self, msg, *args, **kwargs):
        adjustKwarg(kwargs)
        self.log(logging.DEBUG, msg, *args, **kwargs)


def loggedProcess(queue, mpKey, func, *args, **kwargs):
    MPLogger.log_queue = queue
    MPLogger.mpKey = mpKey
    logging.setLoggerClass(MPLogger)
    # monkey patch root logger and already defined loggers
    logging.root.__class__ = MPLogger
    for logger in logging.Logger.manager.loggerDict.values():
        if not isinstance(logger, logging.PlaceHolder):
            logger.__class__ = MPLogger
    func(*args, **kwargs)

# Basic functions to mimic logging.debug type functions but for mpLogging
# If not using loggedProcess then shouldn't be using mpLogging funcs


def critical(msg, *args, **kwargs):
    logging.getLogger().mpCritical(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    logging.getLogger().mpError(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    logging.getLogger().mpWarning(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    logging.getLogger().mpInfo(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    logging.getLogger().mpDebug(msg, *args, **kwargs)
