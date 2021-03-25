from .uiSettings import DISPLAY_TAB_UI_FILE

from .util import loadingUtil

from ..commonUtil import pathUtil

from PySide6 import QtWidgets, QtCore, QtGui


ITEM_ROLE = QtCore.Qt.UserRole


class displayTab(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + DISPLAY_TAB_UI_FILE, parent=self)

        self.m_itemModel = QtGui.QStandardItemModel(self)
        self.ui.listView.setModel(self.m_itemModel)

        self.ui.addButton.clicked.connect(self.slotAddButton)
        self.ui.deleteButton.clicked.connect(self.slotDeleteButton)
        self.ui.listView.clicked.connect(self.slotItemChanged)

    @QtCore.Slot()
    def slotAddButton(self):
        # Override this function to add item
        pass

    @QtCore.Slot()
    def slotDeleteButton(self):
        # self.ui.listWidget.takeItem(self.ui.listWidget.currentRow())
        pass

    def slotItemChanged(self, index):
        """
        Connected to clicked of QListView
        Passes in QModelIndex index of clicked location in QListView
        """
        displayWidget = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(displayWidget)
        displayWidget.setLayout(layout)
        innerWidget = None
        modelItem = self.m_itemModel.item(index.row())
        text = self.m_itemModel.data(index)
        # check if subclass has display item implemented otherwise default
        try:
            item = modelItem.data(ITEM_ROLE)
            innerWidget = self.displayItem(item, displayWidget)
        except AttributeError as e:
            print("Error displaying Item: ")
            print(e)
            innerWidget = QtWidgets.QLabel(text)
        if innerWidget is not None:
            layout.addWidget(innerWidget)

        self.ui.scrollArea.setWidget(displayWidget)

    def loadItems(self, itemDict):
        for key, value in itemDict.items():
            modelItem = QtGui.QStandardItem(key)
            modelItem.setData(value, ITEM_ROLE)
            self.m_itemModel.appendRow(modelItem)

    def displayItem(self, item, parent):
        """
        Tries to display the item based off config in the item, otherwise does nothing
        """
        try:
            item.m_config
        except AttributeError as e:
            print("Item does not have config, cannot display through default function")
            print(e)
        else:
            # Display item using stored config
            treeView = QtWidgets.QTreeView(parent)
            treeModel = QtGui.QStandardItemModel(parent)
            parentItem = treeModel.invisibleRootItem()
            recurseItem(parentItem, item.m_config)
            treeView.setModel(treeModel)
            treeView.expandAll()
            return treeView


def recurseItem(item, value):
    if type(value) is dict:
        for key, val in value.items():
            child = QtGui.QStandardItem()
            child.setText(str(key))
            item.appendRow(child)
            recurseItem(child, val)
    elif type(value) is list:
        for val in value:
            child = QtGui.QStandardItem()
            item.appendRow(child)
            if type(val) is dict:
                child.setText('[dict]')
                recurseItem(child, val)
            elif type(val) is list:
                child.setText('[list]')
                recurseItem(child, val)
            else:
                child.setText(str(val))
    else:
        child = QtGui.QStandardItem()
        child.setText(str(value))
        item.appendRow(child)
