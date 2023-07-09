from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtWidgets import QMessageBox, QLabel

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


class CustomQMessageBox:
    def _init_ui(self, dialog: QMessageBox, title: str, label: str, icon_path: str):
        icon = QIcon()
        icon.addPixmap(QPixmap("ui/gui/resources/main.ico"), QIcon.Mode.Normal, QIcon.State.Off)
        dialog.setWindowIcon(icon)
        dialog.setWindowTitle(title)
        dialog_text_label = dialog.findChild(QLabel, "qt_msgbox_label")
        dialog_text_label.setStyleSheet("* { font-size: 16px; margin-top: 20;  margin-left: 10; margin-right: 20}")
        dialog.setText(label)
        icon = QPixmap(icon_path).scaledToHeight(96, Qt.TransformationMode.SmoothTransformation)
        dialog.setIconPixmap(icon)

    @classmethod
    def _get_dialog(cls, icon: QMessageBox.Icon, parent, title: str, label: str, icon_path: str, buttons):
        dialog = QMessageBox(icon, title, label, buttons, parent)
        cls._init_ui(cls, dialog, title, label, icon_path)
        return dialog

    @classmethod
    def critical(cls, parent, title, label, buttons=QMessageBox.StandardButton.Ok) -> QMessageBox:
        return cls._get_dialog(QMessageBox.Icon.Critical, parent, title, label, "ui/gui/resources/messages/error.png", buttons)

    @classmethod
    def information(cls, parent, title, label, buttons=QMessageBox.StandardButton.Ok) -> QMessageBox:
        return cls._get_dialog(QMessageBox.Icon.Information, parent, title, label, "ui/gui/resources/messages/information.png", buttons)

    @classmethod
    def warning(cls, parent, title, label, buttons=QMessageBox.StandardButton.Ok) -> QMessageBox:
        return cls._get_dialog(QMessageBox.Icon.Warning, parent, title, label, "ui/gui/resources/messages/warning.png", buttons)

    @classmethod
    def question(cls, parent, title, label, buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) -> QMessageBox:
        return cls._get_dialog(QMessageBox.Icon.Question, parent, title, label, "ui/gui/resources/messages/question.png", buttons)

    @classmethod
    def done(cls, parent, title, label, buttons=QMessageBox.StandardButton.Close) -> QMessageBox:
        return cls._get_dialog(QMessageBox.Icon.NoIcon, parent, title, label, "ui/gui/resources/messages/done.png", buttons)
