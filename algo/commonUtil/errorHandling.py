import traceback
import sys
import logging

"""
Algo standardized error logging
"""


def printTraceback(title):
    print(title)
    print("-"*60)
    traceback.print_exc(file=sys.stdout)
    print("-"*60)


def warning(title, description=None):
    logging.warning(" " + title)
    if description:
        logging.warning(" " + description)
