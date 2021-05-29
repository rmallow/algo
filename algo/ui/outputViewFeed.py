from .outputView import outputView
from .uiSettings import OUTPUT_VIEW_FEED_UI_FILE

from .util import loadingUtil

from ..commonUtil import pathUtil
from ..commonGlobals import ITEM, TYPE

from PySide6 import QtCore


class outputViewFeed(outputView):
    def __init__(self, outputViewModel, selectionSettings, parent=None):
        super().__init__(outputViewModel, parent)

        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + OUTPUT_VIEW_FEED_UI_FILE, parent=self)

        self.setup()
        self.ui.tableView.setModel(self.outputViewModel)
        self.ui.itemLabel.setText(selectionSettings[ITEM] + " - " + selectionSettings[TYPE])

    @QtCore.Slot()
    def updateOnLoad(self):
        pass
