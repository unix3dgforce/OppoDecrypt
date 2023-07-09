from PyQt6.QtWidgets import QApplication

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


class App(QApplication):
    def __init__(self):
        QApplication.__init__(self, [])
        self.setStyle("Fusion")
