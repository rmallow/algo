from ..backEnd.message import message

import typing

from PySide6 import QtCore

_loggingColumns = ["Severity", "Source", "Title", "Description"]


class loggingModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logMessages = []

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.logMessages)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(_loggingColumns)

    def data(self, index: QtCore.QModelIndex, role: int) -> typing.Any:
        """
        Override QAbstractTableModel data for displaying pandas dataframe data
        """
        if role == QtCore.Qt.DisplayRole:
            return self.logMessages[index.row()][index.column()]
        else:
            return None

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int) -> typing.Any:
        """
        Override QAbstractTableModel header data for displaying column/row header based off pandas dataframe
        """
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return _loggingColumns[section]
            else:
                return str(section)
        return None

    def receiveData(self, message: message):
        """
        Recieve the logging message from the main model and parse it into a data structure for the Qt Table Model
        Turn logging message into list and add to main list
        """
        self.beginResetModel()
        #self.beginInsertRows(QtCore.QModelIndex(), len(self.logMessages), len(self.logMessages) + 1)
        messageList = [message.details['levelname']]
        messageList.append("Test Source")
        title = "----"
        if 'title' in message.details:
            title = message.details['title']
        messageList.append(title)
        messageList.append(message.details['msg'])
        self.logMessages.append(messageList)
        #self.endInsertRows()
        self.endResetModel()