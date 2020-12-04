import pandas

from urllib.request import urlopen

def getJsonDataStr(url):
    response = urlopen(url)
    return response.read().decode("utf-8")

def getPandasFromUrl(url, indexName=None, columnFilter=None, removeColumns = None):
    jsonStr = getJsonDataStr(url)
    df = pandas.read_json(path_or_buf=jsonStr)

    colList = df.columns

    #set desired column as index
    if indexName and indexName in colList:
        df = df.set_index(indexName)
        colList = df.columns

    bFiltered = False
    #if filter column is not none, remove all columns that aren't in filter columns
    if columnFilter:
        dropColList = []
        for col in colList:
            if col not in columnFilter:
                dropColList.append(col)

        #not going to drop all columns so make sure they're not the same length
        if len(dropColList) > 0 and len(dropColList) != len(colList):
            bFiltered = True
            df = df.drop(dropColList)

    #remove columns from removeColumns if we didn't already filter
    if not bFiltered and removeColumns:
        dropColList = []
        for col in removeColumns:
            if col in colList:
                dropColList.append(col)
        
        if len(dropColList) > 0:
            df = df.drop(dropColList)

    return df

    
