from ..commonGlobals import PERIOD
from ..commonUtil.keywordUnpacker import keywordUnpacker

import typing

from PySide6 import QtCore
import pandas as pd

PANDAS_MODEL_KEYWORDS_DICT = {PERIOD: None}


class pandasModel(keywordUnpacker, QtCore.QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.df = pd.DataFrame()
        self.unpack(kwargs, PANDAS_MODEL_KEYWORDS_DICT, warn=False)

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.df.index)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.df.columns)

    def data(self, index: QtCore.QModelIndex, role: int) -> typing.Any:
        """
        Override QAbstractTableModel data for displaying pandas dataframe data
        """
        if role == QtCore.Qt.DisplayRole:
            return str(self.df.iloc[index.row(), index.column()])
        else:
            return None

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int) -> typing.Any:
        """
        Override QAbstractTableModel header data for displaying column/row header based off pandas dataframe
        """
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.df.columns[section]
            else:
                try:
                    return self.df.index[section].strftime("%m/%d/%Y, %H:%M:%S")
                except AttributeError:
                    return str(self.df.index[section])
        return None

    def appendRow(self, dataframe):
        """
        Add new rows to the dataframe, if df is empty, resetModel to get column changes
        otherwise just beginInsertRows as it is far more efficient
        """
        if self.period is not None:
            if len(self.df.index) + len(dataframe.index) > self.period:
                # Remove rows so that the combined dataframes won't be more than the period
                self.removeRows(0, (len(self.df.index) + len(dataframe.index)) - self.period)

        resetModel = False
        if len(self.df.index) == 0 or len(self.df.columns) == 0:
            self.beginResetModel()
            resetModel = True
        else:
            self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount() + len(dataframe.index) - 1)
        self.df = self.df.append(dataframe)
        if resetModel:
            self.endResetModel()
        else:
            self.endInsertRows()

    def removeRows(self, rowStart, count):
        """
        Function to remove rows from the dataframe and from the table model
        """
        self.beginRemoveRows(QtCore.QModelIndex(), rowStart, rowStart + count)
        self.df.drop(self.df.index[rowStart:rowStart+count])
        self.endRemoveRows()
