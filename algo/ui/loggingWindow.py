from .uiSettings import LOGGING_WINDOW_UI_FILE
from .loggingModel import loggingModel
from .loggingModel import _loggingColumns
from .util import loadingUtil

from ..commonUtil import pathUtil

import logging
from PySide6 import QtWidgets, QtCore, QtGui


def createRegExpFromSet(stringSet):
    regExp = ""
    if len(stringSet) > 0:
        for string in stringSet:
            regExp += string
            regExp += "|"
        regExp = regExp[:-1]
    else:
        # This regex will never match anything and is intended to be inexpesnive:
        # https://stackoverflow.com/questions/1723182/a-regex-that-will-never-be-matched-by-anything
        regExp = "(?!x)x"
    return regExp


class loggingWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Load UI file and setup
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + LOGGING_WINDOW_UI_FILE)

        self.ui.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.ui.tableView.clicked.connect(self.tableActivated)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.textView.setTextColor(QtGui.QColor(QtCore.Qt.white))
        self.ui.textView.setText("Select a log for more information.")

        self.loggingModel = loggingModel()

        # set up filters and their sets
        # Keys
        self.keysSelected = set()
        self.keyFilter = QtCore.QSortFilterProxyModel(self.loggingModel)
        self.keyFilter.setFilterKeyColumn(_loggingColumns.index("Key"))
        # Group
        self.groupsSelected = set()
        self.groupFilter = QtCore.QSortFilterProxyModel(self.loggingModel)
        self.groupFilter.setFilterKeyColumn(_loggingColumns.index("Group"))
        # Severity
        self.severitiesSelected = set()
        self.severityFilter = QtCore.QSortFilterProxyModel(self.loggingModel)
        self.severityFilter.setFilterKeyColumn(_loggingColumns.index("Severity"))

        # overlay filters on model and set view to top filter
        self.keyFilter.setSourceModel(self.loggingModel)
        self.groupFilter.setSourceModel(self.keyFilter)
        self.severityFilter.setSourceModel(self.groupFilter)

        self.ui.tableView.setModel(self.severityFilter)

        self.setupMenus()

        self.loggingModel.addKey.connect(self.addKey)
        self.loggingModel.addGroup.connect(self.addGroup)

    def tableActivated(self, index: QtCore.QModelIndex):
        """
        Slot for when a row is selected in the model, updates the description tab with that row's data
        """
        self.ui.textView.setText(str(self.loggingModel.logMessages[index.row()][self.loggingModel.columnCount()]))

    def setupMenus(self):
        # Severity Menu
        self.severityMenu = QtWidgets.QMenu(self.ui.severityButton)
        # copy for safety
        copyDict = logging._levelToName.copy()
        for key, val in copyDict.items():
            checked = key > logging.INFO
            self.addStringToMenu(self.severityMenu, val, checked=checked)
            if checked:
                self.severitiesSelected.add(val)
        self.ui.severityButton.setMenu(self.severityMenu)

        # Key and Group Menu both start out blank
        self.keyMenu = QtWidgets.QMenu(self.ui.keyButton)
        self.ui.keyButton.setMenu(self.keyMenu)

        self.groupMenu = QtWidgets.QMenu(self.ui.groupButton)
        self.ui.groupButton.setMenu(self.groupMenu)

        self.updateFilters()

    """
    Following functions add to their respective menu and then call updateFilters
    """

    def addKey(self, key):
        self.keysSelected.add(key)
        self.addStringToMenu(self.keyMenu, key, checked=True)
        self.updateFilters()

    def addGroup(self, group):
        self.groupsSelected.add(group)
        self.addStringToMenu(self.groupMenu, group, checked=True)
        self.updateFilters()

    def addStringToMenu(self, menu, string, checked=False):
        """
        Add a string to a menu, if checked is True then set the item as checked
        """
        check = QtWidgets.QCheckBox(string, menu)
        check.setChecked(checked)
        action = QtWidgets.QWidgetAction(menu)
        action.setDefaultWidget(check)
        check.stateChanged.connect(self.menuItemChecked)
        menu.addAction(action)

    @QtCore.Slot()
    def menuItemChecked(self, state):
        """
        Slot for when an item in the menu is checked/unchecked
        if checked add to its respective set
        if unchecked remove from its respective set
        """
        check = self.sender()
        text = check.text()
        parent = check.parent()
        setToChange = None
        if parent == self.keyMenu:
            setToChange = self.keysSelected
        elif parent == self.groupMenu:
            setToChange = self.groupsSelected
        elif parent == self.severityMenu:
            setToChange = self.severitiesSelected

        if setToChange is not None:
            if state == QtCore.Qt.Unchecked:
                setToChange.remove(text)
            else:
                setToChange.add(text)

        self.updateFilters()

    def updateFilters(self):
        """
        Called when there is a change to the sets that determine what should be shown on the window
        """
        regExp = createRegExpFromSet(self.keysSelected)
        if regExp != self.keyFilter.filterRegularExpression():
            self.keyFilter.setFilterRegularExpression(regExp)

        regExp = createRegExpFromSet(self.groupsSelected)
        if regExp != self.groupFilter.filterRegularExpression():
            self.groupFilter.setFilterRegularExpression(regExp)

        regExp = createRegExpFromSet(self.severitiesSelected)
        if regExp != self.severityFilter.filterRegularExpression():
            self.severityFilter.setFilterRegularExpression(regExp)
