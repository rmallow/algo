import importlib
import logging
import os
import pickle
import yaml


def saveObj(obj, name):
    with open('../obj/' + name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def getConfigDictFromFile(path):
    with open(path) as file:
        return yaml.load(file, yaml.FullLoader)


def pickleConfigFile(path):
    with open(path) as file:
        saveObj(yaml.load(file, yaml.FullLoader), os.path.splitext(os.path.split(path)[1])[0])


def loadFunc(funcConfig):
    module = importlib.import_module(funcConfig['location'])
    if module is not None:
        if hasattr(module, funcConfig['name']):
            return getattr(module, funcConfig['name'])
        else:
            logging.warning("attr not found: " + funcConfig['name'] + "at module: " + funcConfig['location'])
    else:
        logging.warning("module not found: " + funcConfig['location'])
    return None
