import asyncio
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from qasync import QEventLoop, asyncSlot

from core.interfaces import IUserInterface, IExtractor
from core.models import PayloadModel
from core.models.super import MetadataPartitionModel
from ui.gui import AboutDialog
from ui.gui.controllers import ThemasController
from ui.gui.views import MainView

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"

from ui.gui.widget import CustomQMessageBox


class MainWindow(IUserInterface, QMainWindow):
    def __init__(self, app: QApplication):
        super(MainWindow, self).__init__()
        self._app = app
        self._extractors: dict[str, IExtractor] = {}
        self._themas = ThemasController(self._app)

        self.main_window = MainView(self)
        self.main_window.setup()

        self.setFixedSize(self.width(), self.height())
        self._about_dialog = AboutDialog()

        self.main_window.menu_themas_dark_mode_action.triggered.connect(lambda: self._themas.dark_mode(True))
        self.main_window.menu_themas_light_mode_action.triggered.connect(lambda: self._themas.dark_mode(False))
        self.main_window.menu_help_action.triggered.connect(lambda: self._about_dialog.exec())

        self.main_window.tool_btn_input_path.clicked.connect(self._input_path_dialog)
        self.main_window.tool_btn_output_path.clicked.connect(self._output_path_dialog)

        self.main_window.input_path.textChanged.connect(self._parameter_handler)
        self.main_window.output_path.textChanged.connect(self._parameter_handler)

        self.main_window.btn_extract.clicked.connect(self.run)

    @property
    def app(self) -> QApplication:
        return self._app

    @property
    def extractors(self) -> dict[str, IExtractor]:
        return self._extractors

    @extractors.setter
    def extractors(self, value: dict[str, IExtractor]) -> None:
        for item in value.values():
            item.user_interface = self

        self._extractors = value

    def _parameter_handler(self):
        if self.main_window.input_path.text() != "" and self.main_window.output_path.text() != "":
            self.main_window.btn_extract.setEnabled(True)
        else:
            self.main_window.btn_extract.setEnabled(False)

    def _input_path_dialog(self):
        input_path, _ = QFileDialog.getOpenFileName(self, "", Path.cwd().__str__(), "All Firmware (*.ofp *.ops);; OFP Firmware (*.ofp);; OPS Firmware (*.ops)")
        if input_path == "":
            return

        self.main_window.input_path.setText(input_path)

    def _output_path_dialog(self):
        dialog = QFileDialog()
        dialog.setViewMode(QFileDialog.ViewMode.List)
        output_path = dialog.getExistingDirectory(self, "Select Output Directory", Path.cwd().__str__(), QFileDialog.Option.ShowDirsOnly)
        if output_path == "":
            return

        self.main_window.output_path.setText(output_path)

    def choice_build_configuration(self, input_files: list[Path], default_path: Path = None) -> list[Path]:
        pass

    def choice_extraction_partitions(self, partitions: list[MetadataPartitionModel]) -> list[MetadataPartitionModel]:
        pass

    def get_super_map_path(self, input_files: list[Path], default_path: Path = None) -> Path:
        pass

    def get_custom_extract_folder(self, output_folder: Path) -> Path:
        pass

    def launch_confirmation(self, message: str, payload: PayloadModel, forced: bool = False) -> bool:
        pass

    def get_extractors_chain(self, key: str) -> IExtractor:
        _extractor = self._extractors.get(key)
        _extractor.set_next_extractor(self._extractors.get("sparse")).set_next_extractor(self._extractors.get("super"))
        return _extractor

    @asyncSlot()
    async def run(self):
        extractor = self.get_extractors_chain('ops_qualcomm')

        input_file = Path(self.main_window.input_path.text())
        output_dir = Path(self.main_window.output_path.text())

        extractor.run(PayloadModel(input_file=input_file, output_dir=output_dir))
