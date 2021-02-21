import yaml
import pickle
import os


def saveObj(obj, name):
    with open('../obj/' + name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def getConfigDictFromFile(path):
    with open(path) as file:
        return yaml.load(file, yaml.FullLoader)


def pickleConfigFile(path):
    with open(path) as file:
        saveObj(yaml.load(file, yaml.FullLoader), os.path.splitext(os.path.split(path)[1])[0])
