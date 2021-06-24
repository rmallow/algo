import importlib
import logging
import os
import pickle
import yaml
import configparser
import re
from ...commonUtil import mpLogging

VALUES_SECTION = 'Values'


class configLoader():
    def __init__(self, settingsFile=None):
        # can look up full key value or just further in
        # Only using section name if it exists, otherwise not including
        # MainSettingsKey.SectionName.Key = Value
        # MainSettingsKey.Key = Value
        # SetcionName.Key = Value
        # Key = Value
        self.valueDict = {}
        if settingsFile:
            self.loadValues(settingsFile)

    def loadValues(self, settingsFile):
        parser = configparser.ConfigParser()
        parser.read(settingsFile)
        if VALUES_SECTION in parser.sections():
            valuesTupleList = parser.items(VALUES_SECTION)
            for settingsKey, settingsValue in valuesTupleList:
                settingsKey = settingsKey.lower()
                if os.path.exists(settingsValue):
                    parser = configparser.ConfigParser()
                    with open(settingsValue) as stream:
                        # appending a section just in case a section was never passed in
                        parser.read_string("[top]\n" + stream.read())
                    for section in parser.sections():
                        for fileKey, fileValue in parser.items(section):
                            self.valueDict[str(settingsKey)+"."+str(fileKey)] = fileValue
                            if section != "top":
                                self.valueDict[str(settingsKey)+"."+str(section)+"." + str(fileKey)] = fileValue
                                self.valueDict[str(section)+"." + str(fileKey)] = fileValue
                            self.valueDict[str(fileKey)] = fileValue
                else:
                    mpLogging.warning("Path provided but not found",
                                      description=f"Key: {settingsKey} Value/Path: {settingsValue}")
        else:
            print("No default values provided")

    def matchReplace(self, reMatch):
        string = reMatch.group(0)
        if len(string) > 3:
            string = string[2: len(string) - 1]
            # need to use lower() becuase configParser converst keys to lower
            if string.lower() in self.valueDict:
                return self.valueDict[string.lower()]
        return string

    def recurseDictForFunc(self, container, parentKey, item):
        if parentKey.lower().endswith("func"):
            if isinstance(container, dict):
                container[parentKey] = loadFunc(item)
            elif isinstance(container, list):
                for index, value in enumerate(container):
                    if value == item:
                        container[index] = loadFunc(item)
        elif isinstance(item, dict):
            for key, value in item.items():
                self.recurseDictForFunc(item, key, value)
        elif isinstance(item, list):
            for value in item:
                self.recurseDictForFunc(item, parentKey, value)

    def recurseDictForFuncMain(self, d):
        for key, value in d.items():
            self.recurseDictForFunc(d, key, value)

    def loadAndReplaceYamlFile(self, path):
        contents = {}
        try:
            fileStrings = ""
            with open(path) as file:
                fileStrings = file.read()
            if len(fileStrings) > 0:
                yamlReady = re.sub(r"\$\[[^]]*\]", self.matchReplace, fileStrings)
                contents = yaml.safe_load(yamlReady)
                self.recurseDictForFuncMain(contents)
        except OSError:
            mpLogging.error("Exception loading file", descripti=f"File: {path}")
        return contents


def saveObj(obj, name):
    with open('../obj/' + name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def getDictFromYmlFile(path):
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


def getKeyValueIni(iniFile):
    valueDict = {}
    parser = configparser.ConfigParser()
    with open(iniFile) as stream:
        # appending a section just in case a section was never passed in
        parser.read_string("[top]\n" + stream.read())
    for section in parser.sections():
        for fileKey, fileValue in parser.items(section):
            valueDict[str(fileKey)] = fileValue
    return valueDict
