import importlib
import logging
import os
import pickle
import yaml
import configparser
import re
from ...commonUtil import errorHandling

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
            print("No default values provided")

    def matchReplace(self, reMatch):
        string = reMatch.group(0)
        if len(string) > 3:
            string = string[2:len(string)-1]
            if string in self.valueDict:
                return self.valueDict[string]
        return string

    def loadAndReplaceYamlFile(self, path):
        try:
            fileStrings = ""
            with open(path) as file:
                fileStrings = file.read()
            if len(fileStrings) > 0:
                yamlReady = re.sub(r"\$\[[^]]*\]", self.matchReplace, fileStrings)
                return yaml.safe_load(yamlReady)
        except OSError:
            errorHandling.printTraceback("Exception loading file: ")
        return {}


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
