from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from ui.gui.views import AboutView

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"
__all__ = ["AboutDialog"]


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self._dialog = AboutView(self)
        self._dialog.setup()
        self.setWindowFlag(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setFixedSize(self.width(), self.height())
        self._dialog.btn_close.clicked.connect(lambda: self.close())
