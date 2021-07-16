from ..commonGlobals import UI_GROUP, SEND_TIME, RECEIVE_TIME, BACK_TIME
from ..commonUtil import mpLogging

from ..backEnd.message import message

from PySide6 import QtGui, QtCore

SEND_ROW = 0
RECEIVE_ROW = 1
BACK_ROW = 2

_specialHandling = {SEND_TIME: SEND_ROW, RECEIVE_TIME: RECEIVE_ROW, BACK_TIME: BACK_ROW}

ROW_TO_KEY_MAP_ROLE = QtCore.Qt.UserRole + 1


class statusModel(QtGui.QStandardItemModel):
    def receiveData(self, msg: message):
        root = self.invisibleRootItem()
        codeItem = None
        findList = self.findItems(msg.key.sourceCode)
        if len(findList) == 0:
            # code has not been added to table yet, add it now
            codeItem = QtGui.QStandardItem(msg.key.sourceCode)
            codeItem.setData({}, role=ROW_TO_KEY_MAP_ROLE)
            root.appendRow(codeItem)
        elif len(findList) == 1:
            codeItem = findList[0]
        else:
            mpLogging.error("Multiple items with same code found",
                            description=f"Code: {msg.key.sourceCode}", group=UI_GROUP)

        # Set the status color based on the presence of certain fields in details
        statusColor = QtCore.Qt.red
        if RECEIVE_TIME in msg.details:
            statusColor = QtCore.Qt.green
        codeItem.setBackground(QtGui.QBrush(statusColor))

        rowToKeyMap = codeItem.data(ROW_TO_KEY_MAP_ROLE)
        for key in _specialHandling:
            if key in msg.details:
                detailItem = QtGui.QStandardItem(f"{key}: {msg.details[key]}")
                codeItem.setChild(_specialHandling[key], detailItem)

        # Iterate through details and add the items
        for key, value in msg.details.items():
            if key not in _specialHandling:
                detailItem = QtGui.QStandardItem(f"{key}: {value}")
                if key in rowToKeyMap:
                    codeItem.setChild(rowToKeyMap[key], detailItem)
                else:
                    codeItem.appendRow(detailItem)
                    rowToKeyMap[key] = codeItem.rowCount()-1
        codeItem.setData(rowToKeyMap, ROW_TO_KEY_MAP_ROLE)
            