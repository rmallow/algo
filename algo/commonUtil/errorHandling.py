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
    print("-" * 60)


def warning(title, description):
    logging.warning(title)
    logging.warning(description)
