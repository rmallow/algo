
import typing

from PySide6 import QtCore
import pandas as pd


class pandasModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame()

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
