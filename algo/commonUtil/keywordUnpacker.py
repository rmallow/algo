from . import errorHandling
from .multiBase import multiBase

"""
Pass in a dict of keywords and their default values that you want to unpack as attributes of the class
Or unpack all keywords of a dict

If you call unpack more than once, older values can be overwritten obviously

Class inherits from multiBase and is safe for multiple inheritance
"""


class keywordUnpacker(multiBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def unpack(self, keywordDict, keywordDefault,  required=[], warn=True):
        """
        @brief: Unpack a dict as attributes of the class
                If keyword from keywordDict is not in keywordDefault then it will not be unpacked
                Remaining keys in keywordDefault are set as class attributes by their dict values

        @param: keywordDict - dict to unpack
        @param: keywordDefault - dictionary of keys to unpack with the dict[key] as the default value
        @param: warn - if true then warn the user if a keyword default key is missing
        @param: required - list of parameters that are required to be passed in, if they aren't it will assert
        """
        keywordsDefaultCopy = keywordDefault.copy()
        requiredListCopy = required.copy()
        for k, v in keywordDict.items():
            if k in keywordsDefaultCopy:
                setattr(self, k, v)
                del keywordsDefaultCopy[k]
                if k in requiredListCopy:
                    requiredListCopy.remove(k)
            elif k in requiredListCopy:
                setattr(self, k, v)
                requiredListCopy.remove(k)

        if len(requiredListCopy) > 0:
            errorHandling.logAssert("Missing required parameter in defention of " + str(self.__class__.__name__),
                                    description="Missing required parameters: " + str(requiredListCopy))

        if warn and keywordsDefaultCopy:
            errorHandling.warning("Missing keyword in defenition of " + str(self.__class__.__name__),
                                  description="Keywords to set as default: " + str(list(keywordsDefaultCopy.keys())))

        for kDefault, vDefault in keywordsDefaultCopy.items():
            setattr(self, kDefault, vDefault)

    def unpackAll(self, keywordDict):
        for k, v in keywordDict.items():
            setattr(self, k, v)
