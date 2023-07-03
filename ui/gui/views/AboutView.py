from PyQt6.QtCore import Qt, QRect, QMetaObject, QCoreApplication
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton

from ui.gui.views import BaseView

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


class AboutView(BaseView):
    def __init__(self, dialog: QDialog):
        self.dialog = dialog
        self.app_name: QLabel | None = None
        self.app_version: QLabel | None = None
        self.btn_close: QPushButton | None = None

    def setup(self) -> None:
        self.dialog.setObjectName("about_dialog")
        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.dialog.resize(387, 200)
        icon = QIcon()
        icon.addPixmap(QPixmap("ui/gui/resources/main.ico"), QIcon.Mode.Normal, QIcon.State.Off)
        self.dialog.setWindowIcon(icon)
        self.dialog.setSizeGripEnabled(False)
        self.dialog.setModal(False)

        self.app_name = QLabel(self.dialog)
        self.app_name.setGeometry(QRect(170, 16, 151, 31))
        self.app_name.setFont(self.set_font(size=13, bold=True, weight=100))
        self.app_name.setObjectName('app_name')

        self.app_version = QLabel(self.dialog)
        self.app_version.setGeometry(QRect(170, 45, 291, 120))
        self.app_version.setFont(self.set_font(size=10, bold=False, weight=50))
        self.app_version.setObjectName('app_version')

        app_logo = QLabel(self.dialog)
        app_logo.setGeometry(QRect(10, 35, 151, 121))
        app_logo.setText("")
        app_logo.setTextFormat(Qt.TextFormat.PlainText)
        app_logo.setPixmap(QPixmap("ui/gui/resources/logo/logo.png").scaledToHeight(128, Qt.TransformationMode.SmoothTransformation))
        app_logo.setObjectName('app_logo')

        self.btn_close = QPushButton(self.dialog)
        self.btn_close.setGeometry(QRect(280, 165, 91, 21))
        self.btn_close.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.btn_close.setObjectName("btn_close")

        self.translate()

        QMetaObject.connectSlotsByName(self.dialog)

    def translate(self) -> None:
        translate = QCoreApplication.translate
        self.dialog.setWindowTitle(translate("Dialog", "About Ops/Ofp Extractor"))
        self.app_name.setText(translate("Dialog", "Ops/Ofp Extractor"))
        self.app_version.setText(translate("Dialog", "<html><head/><body><p><b>Version 1.0.0</b></p>"
                                                     "<p>Thanks: <b><a href='https://github.com/bkerler'>Bjoern Kerler</a></b><br>"
                                                     "<br>Copyright &copy; 2023 <br><b>Sergey K</b> (a.k.a unix3dgforce)</p></body></html>"))
        self.btn_close.setText(translate("Dialog", "Close"))
