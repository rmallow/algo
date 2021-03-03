import os


def getFileDirPath(filename):
    """
    @brief: pass in file name and get the path to the dir of that file
        use __file__        useful for getting dir path in subdirctories
    """

    dirPath, _ = os.path.split(os.path.realpath(filename))
    return dirPath
