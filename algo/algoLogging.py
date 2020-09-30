import traceback
import logging
import sys

def formatTraceback(tracebackWarning):
    formattedWarning = ""
    for level in tracebackWarning:
        if isinstance(level, traceback.FrameSummary) and  level.filename and level.lineno:
            tokens = level.filename.split("/")
            formattedWarning += tokens[-2] + " -> " + tokens[-1] + " Line Number: " + str(level.lineno) + "\n"    
        else:
            formattedWarning += "unknown traceback level format\n"
    return
    
def exceptionTraceback(e):
    logging.warning(e)
    _, _, exc_traceback = sys.exc_info()
    warning = traceback.extract_tb(exc_traceback)
    logging.warning(formatTraceback(warning))