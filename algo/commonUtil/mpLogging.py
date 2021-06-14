import logging

_extraKwargs = ['title', 'source']

# larger than the predifined logging values so we can
# check if more than logging.CRITICAL to see if special
MP_NOTSET = 60
MP_DEBUG = 70
MP_INFO = 80
MP_WARNING = 90
MP_ERROR = 100
MP_CRITICAL = 110

_mpLevelToName = {
    MP_NOTSET: 'NOTSET',
    MP_DEBUG: 'DEBUG',
    MP_INFO: 'INFO',
    MP_WARNING: 'WARNING',
    MP_ERROR: 'ERROR',
    MP_CRITICAL: 'CRITICAL'
}

logging.addLevelName(MP_NOTSET, _mpLevelToName[MP_NOTSET])
logging.addLevelName(MP_DEBUG, _mpLevelToName[MP_DEBUG])
logging.addLevelName(MP_INFO, _mpLevelToName[MP_INFO])
logging.addLevelName(MP_WARNING, _mpLevelToName[MP_WARNING])
logging.addLevelName(MP_ERROR, _mpLevelToName[MP_ERROR])
logging.addLevelName(MP_CRITICAL, _mpLevelToName[MP_CRITICAL])


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

    def isEnabledFor(self, level):
        return True

    def handle(self, record):
        if record.levelno > logging.CRITICAL:
            ei = record.exc_info
            if ei:
                # to get traceback text into record.exc_text
                logging._defaultFormatter.format(record)
                record.exc_info = None  # not needed any more
            d = dict(record.__dict__)
            d['msg'] = record.getMessage()
            d['args'] = None
            self.log_queue.put(d)
        else:
            super().handle(record)

    def log(self, level, msg, *args, **kwargs):
        for kwarg in _extraKwargs:
            if kwarg in kwargs:
                if 'extra' not in kwargs:
                    kwargs['extra'] = {}
                kwargs['extra'][kwarg] = kwargs[kwarg]
                del kwargs[kwarg]
        super().log(level, msg, *args, **kwargs)

    def mpCritical(self, msg, *args, **kwargs):
        self.log(MP_CRITICAL, msg, *args, **kwargs)

    def mpError(self, msg, *args, **kwargs):
        self.log(MP_ERROR, msg, *args, **kwargs)

    def mpWarning(self, msg, *args, **kwargs):
        self.log(MP_WARNING, msg, *args, **kwargs)

    def mpInfo(self, msg, *args, **kwargs):
        self.log(MP_INFO, msg, *args, **kwargs)

    def mpDebug(self, msg, *args, **kwargs):
        self.log(MP_DEBUG, msg, *args, **kwargs)


def loggedProcess(queue, func, *args, **kwargs):
    MPLogger.log_queue = queue
    logging.setLoggerClass(MPLogger)
    # monkey patch root logger and already defined loggers
    logging.root.__class__ = MPLogger
    for logger in logging.Logger.manager.loggerDict.values():
        if not isinstance(logger, logging.PlaceHolder):
            logger.__class__ = MPLogger
    func(*args, **kwargs)


# Basic functions to mimic logging.debug type functions but for mpLogging

def critical(msg, *args, **kwargs):
    logging.getLogger().log(MP_CRITICAL, msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    logging.getLogger().log(MP_ERROR, msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    logging.getLogger().log(MP_WARNING, msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    logging.getLogger().log(MP_INFO, msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    logging.getLogger().log(MP_DEBUG, msg, *args, **kwargs)
