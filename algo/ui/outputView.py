from PySide6 import QtWidgets


class outputView(QtWidgets.QWidget):
    def __init__(self, outputViewModel, parent=None):
        super().__init__(parent)
        self.outputViewModel = outputViewModel

    def setup(self):
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.ui)
        self.setLayout(self.mainLayout)
        self.setMinimumHeight(self.ui.height())
