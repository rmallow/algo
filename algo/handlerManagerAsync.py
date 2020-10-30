from algo.handler import handler
import multiprocessing as mp
import importlib
import queue
import algo.message as msg
import logging

def _loadCalcFunc(calcFuncConfig):
    return getattr(importlib.import_module(calcFuncConfig['location']),calcFuncConfig['name'])

