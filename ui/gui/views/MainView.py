from PyQt6.QtCore import Qt, QCoreApplication, QRect, QSize
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QWidget, QGroupBox, QLabel, QStatusBar, QComboBox, QLineEdit, QToolButton, \
    QPushButton, QTextEdit

from ui.gui.views import BaseView

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


class MainView(BaseView):
    def __init__(self, main: QMainWindow):
        self.main = main
        self.menu: QMenuBar | None = None
        self.menu_help: QMenu | None = None
        self.menu_themas: QMenu | None = None
        self.menu_themas_dark_mode_action: QAction | None = None
        self.menu_themas_light_mode_action: QAction | None = None
        self.menu_help_action: QAction | None = None
        self.label_cpu_type: QLabel | None = None
        self.statusbar: QStatusBar | None = None
        self.combobox_cpu_type: QComboBox | None = None
        self.label_input_path: QLabel | None = None
        self.input_path: QLineEdit | None = None
        self.tool_btn_input_path: QToolButton | None = None
        self.label_output_path: QLabel | None = None
        self.output_path: QLineEdit | None = None
        self.tool_btn_output_path: QToolButton | None = None
        self.btn_extract: QPushButton | None = None
        self.log: QTextEdit | None = None

    def setup(self) -> None:
        self.main.setObjectName("main")
        self.main.setWindowModality(Qt.WindowModality.NonModal)
        self.main.resize(580, 500)
        icon = QIcon()
        icon.addPixmap(QPixmap("ui/gui/resources/main.ico"), QIcon.Mode.Normal, QIcon.State.Off)
        self.main.setWindowIcon(icon)

        self.menu = QMenuBar(self.main)
        self.menu.setGeometry(QRect(0, 0, 580, 20))
        self.menu.setObjectName("menu")

        self.menu_themas = QMenu(self.menu)
        self.menu_themas.setObjectName("menu_themas")

        self.menu_themas_dark_mode_action = QAction(self.main)
        icon = QIcon()
        icon.addPixmap(QPixmap("ui/gui/resources/menu/dark_mode_on.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_themas_dark_mode_action.setIcon(icon)
        self.menu_themas_dark_mode_action.setObjectName("action_dark_mode")
        self.menu_themas.addAction(self.menu_themas_dark_mode_action)

        self.menu_themas_light_mode_action = QAction(self.main)
        icon = QIcon()
        icon.addPixmap(QPixmap("ui/gui/resources/menu/dark_mode_off.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_themas_light_mode_action.setIcon(icon)
        self.menu_themas_light_mode_action.setObjectName("action_light_mode")
        self.menu_themas.addAction(self.menu_themas_light_mode_action)

        self.menu_help = QMenu(self.menu)
        self.menu_help.setObjectName("menu_help")

        self.menu_help_action = QAction(self.main)
        icon = QIcon()
        icon.addPixmap(QPixmap("ui/gui/resources/menu/help.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_help_action.setIcon(icon)
        self.menu_help_action.setMenuRole(QAction.MenuRole.AboutRole)
        self.menu_help_action.setObjectName("action_help")
        self.menu_help.addAction(self.menu_help_action)

        self.menu.addAction(self.menu_themas.menuAction())
        self.menu.addAction(self.menu_help.menuAction())
        self.main.setMenuBar(self.menu)

        central_widget = QWidget(self.main)
        central_widget.setObjectName("central_widget")

        group_box = QGroupBox(central_widget)
        group_box.setGeometry(QRect(5, 5, 570, 110))
        group_box.setObjectName("group_box")

        self.label_cpu_type = QLabel(group_box)
        self.label_cpu_type.setGeometry(QRect(10, 10, 100, 20))
        self.label_cpu_type.setObjectName("label_cpu_type")

        self.combobox_cpu_type = QComboBox(group_box)
        self.combobox_cpu_type.setGeometry(QRect(110, 10, 100, 20))
        self.combobox_cpu_type.setObjectName("cpu_type")

        self.label_input_path = QLabel(group_box)
        self.label_input_path.setGeometry(QRect(10, 44, 100, 20))
        self.label_input_path.setObjectName("label_input_path")

        self.input_path = QLineEdit(group_box)
        self.input_path.setGeometry(QRect(110, 44, 320, 20))
        self.input_path.setReadOnly(True)
        self.input_path.setObjectName("input_path")

        self.tool_btn_input_path = QToolButton(group_box)
        self.tool_btn_input_path.setGeometry(QRect(435, 44, 20, 20))
        self.tool_btn_input_path.setObjectName("tool_btn_input_path")

        self.label_output_path = QLabel(group_box)
        self.label_output_path.setGeometry(QRect(10, 74, 100, 20))
        self.label_output_path.setObjectName("label_output_path")

        self.output_path = QLineEdit(group_box)
        self.output_path.setGeometry(QRect(110, 74, 320, 20))
        self.output_path.setReadOnly(True)
        self.output_path.setObjectName("output_path")

        self.tool_btn_output_path = QToolButton(group_box)
        self.tool_btn_output_path.setGeometry(QRect(435, 74, 20, 20))
        self.tool_btn_output_path.setObjectName("tool_btn_input_path")

        self.btn_extract = QPushButton(group_box)
        self.btn_extract.setGeometry(QRect(460, 45, 100, 50))
        self.btn_extract.setIconSize(QSize(24, 24))
        icon = QIcon()
        icon.addPixmap(QPixmap("ui/gui/resources/button.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_extract.setIcon(icon)
        self.btn_extract.setObjectName("btn_execute")
        self.btn_extract.setFont(self.set_font(size=15, bold=True))
        self.btn_extract.setEnabled(True)

        self.log = QTextEdit(central_widget)
        self.log.setGeometry(QRect(5, 120, 570, 330))
        self.log.setObjectName("log")

        self.main.setCentralWidget(central_widget)

        self.statusbar = QStatusBar(self.main)
        self.statusbar.setObjectName("statusbar")
        self.main.setStatusBar(self.statusbar)

        self.translate()

    def translate(self) -> None:
        translate = QCoreApplication.translate
        self.main.setWindowTitle(translate("main", "Ops/Ofp Extractor"))
        self.menu_themas.setTitle(translate("main", "Themas"))
        self.menu_themas_dark_mode_action.setText(translate("main", "Dark Mode"))
        self.menu_themas_dark_mode_action.setShortcut(translate("main", "Ctrl+D"))
        self.menu_themas_light_mode_action.setText(translate("main", "Normal Mode"))
        self.menu_themas_light_mode_action.setShortcut(translate("main", "Ctrl+L"))
        self.menu_help.setTitle(translate("main", "Help"))
        self.menu_help_action.setText(translate("main", "About"))
        self.menu_help_action.setShortcut(translate("main", "Ctrl+I"))
        self.label_cpu_type.setText(translate("main", "Select CPU Type :"))
        self.combobox_cpu_type.addItem(translate("main", "Qualcomm"))
        self.combobox_cpu_type.addItem(translate("main", "MTK"))
        self.label_input_path.setText(translate("main", "Input Firmware :"))
        self.tool_btn_input_path.setText(translate("main", "..."))
        self.label_output_path.setText(translate("main", "Output Directory :"))
        self.tool_btn_output_path.setText(translate("main", "..."))
        self.btn_extract.setText(translate("main", "Extract"))
