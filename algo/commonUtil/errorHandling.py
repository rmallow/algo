import traceback
import sys


def printTraceback(title):
    print(title)
    print("-"*60)
    traceback.print_exc(file=sys.stdout)
    print("-" * 60)
