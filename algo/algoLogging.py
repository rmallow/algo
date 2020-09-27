import traceback

def formatTraceback(tracebackWarning):
    formattedWarning = ""
    for level in tracebackWarning:
        if isinstance(level, traceback.FrameSummary) and  level.filename and level.lineno:
            tokens = level.filename.split("/")
            formattedWarning += tokens[-2] + " -> " + tokens[-1] + " Line Number: " + str(level.lineno) + "\n"    
        else:
            formattedWarning += "unknown traceback level format\n"
    return formattedWarning