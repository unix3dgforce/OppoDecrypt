from __future__ import annotations

from pathlib import Path
from typing import Any

import jinja2
from PyQt6.QtCore import QThread, QMutex, QWaitCondition
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

from core.interfaces import IExtractor, ILogService
from core.models import PayloadModel, ConfigurationModel, LogMessageModel, LogLevel
from core.models.super import MetadataPartitionModel
from core.validators import SupersImgCompareCsvGuiValidator
from exceptions import ValidationError
from ui.gui import AboutDialog
from ui.gui.controllers import ThemasController
from ui.gui.views import MainView
from ui.gui.widgets import CustomQMessageBox, ConfigurationDialog, PartitionDialog
from ui.gui.workers import ExtractWorker

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


class MainWindow(QMainWindow):
    _mutex = QMutex()
    _wait_condition = QWaitCondition()

    def __init__(self, app: QApplication, extract_worker: ExtractWorker, configuration: dict[str, Any], logger: ILogService):
        super(MainWindow, self).__init__()
        self._logger = logger
        self._app = app
        self._extractors: dict[str, IExtractor] = {}
        self._messages: list[LogMessageModel] = []

        self.extract_worker = extract_worker
        self._thread = QThread()
        self._configure_thread_extract_worker(self.extract_worker)
        self._thread.start()

        self._themas = ThemasController(self._app)
        self._themas.change_palette.connect(self._update_style_log)

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

        self._log_renders = {
            "one":  jinja2.Environment(loader=jinja2.FileSystemLoader(Path(__file__).parent / "resources/templates"),
                                       trim_blocks=True,
                                       lstrip_blocks=True).get_template("log_message.html"),
            "many": jinja2.Environment(loader=jinja2.FileSystemLoader(Path(__file__).parent / "resources/templates"),
                                       trim_blocks=True,
                                       lstrip_blocks=True).get_template("log_messages.html")
        }

        self._themas.dark_mode(configuration.get("dark_mode", False))

    @property
    def app(self) -> QApplication:
        return self._app

    @property
    def extractors(self) -> dict[str, IExtractor]:
        return self._extractors

    @extractors.setter
    def extractors(self, value: dict[str, IExtractor]) -> None:
        self._extractors = value

    def _configure_thread_extract_worker(self, extract_worker: ExtractWorker):
        extract_worker.moveToThread(self._thread)
        extract_worker.start.connect(self.extract_worker.run)

        extract_worker.ask_continue_execution_question.connect(self._show_dialog_launch_confirmation)
        extract_worker.ask_extract_partitions_folder.connect(self._show_dialog_custom_extract_partitions_path)
        extract_worker.ask_super_map_path.connect(self._show_dialog_super_map_path)
        extract_worker.ask_configuration.connect(self._show_dialog_choice_build_configuration)
        extract_worker.ask_partition.connect(self._show_dialog_choice_partition)
        extract_worker.log_updated.connect(self._update_log_view)
        extract_worker.finished.connect(self._is_finished)
        self._thread.finished.connect(self._thread.deleteLater)

    def _is_finished(self):
        CustomQMessageBox.done(self, "Extract completed", f"Firmware extraction completed").exec()
        self._toggle_control_element_enable(True)

    def _input_path_dialog(self):
        input_path, _ = QFileDialog.getOpenFileName(self, "", str(Path.cwd()),
                                                    "All Firmware (*.ofp *.ops);; OFP Firmware (*.ofp);; OPS Firmware (*.ops)")
        if input_path == "":
            return

        self.main_window.input_path.setText(input_path)

    def _output_path_dialog(self):
        dialog = QFileDialog()
        dialog.setViewMode(QFileDialog.ViewMode.List)
        output_path = dialog.getExistingDirectory(self, "Select Output Directory", str(Path.cwd()), QFileDialog.Option.ShowDirsOnly)
        if output_path == "":
            return

        self.main_window.output_path.setText(output_path)

    def _parameter_handler(self):
        if self.main_window.input_path.text() != "" and self.main_window.output_path.text() != "":
            self.main_window.btn_extract.setEnabled(True)
        else:
            self.main_window.btn_extract.setEnabled(False)

    def _show_dialog_choice_build_configuration(self, configurations: list[ConfigurationModel]):
        configuration = ConfigurationDialog.getConfigurations("Select configuration build", configurations, 2)
        self._wait_condition.wakeOne()
        self.extract_worker.receive_data = configuration

    def _show_dialog_choice_partition(self, partitions: list[MetadataPartitionModel]):
        partition = PartitionDialog.getPartitions("Select extract partitions", partitions, 2)
        self._wait_condition.wakeOne()
        self.extract_worker.receive_data = partition

    def _show_dialog_custom_extract_partitions_path(self, output_dir: Path):
        dialog = QFileDialog()
        dialog.setViewMode(QFileDialog.ViewMode.List)
        output_path = dialog.getExistingDirectory(self, "Select Extract Partitions Directory", str(output_dir), QFileDialog.Option.ShowDirsOnly)
        result = output_dir
        if output_path != "":
            result = Path(output_path)

        self.extract_worker.receive_data = result
        self._wait_condition.wakeOne()

    def _show_dialog_launch_confirmation(self, message: str):
        buttons = CustomQMessageBox.question(self, "Continue extraction", message).exec()
        self.extract_worker.receive_data = buttons == QMessageBox.StandardButton.Yes
        self._wait_condition.wakeOne()

    def _show_dialog_super_map_path(self, input_files: list[Path], default_path: Path):
        while True:
            super_map_path, _ = QFileDialog.getOpenFileName(self, "Choice Super Map", str(default_path) if default_path else str(Path.cwd()),
                                                            "Super Map File (super_map.csv)")
            if super_map_path == "":
                CustomQMessageBox.warning(self, "Choice super map file", "No file selected").exec()
                continue

            try:
                SupersImgCompareCsvGuiValidator(input_files).validate(super_map_path)
                break
            except ValidationError as error:
                CustomQMessageBox.critical(self, "Error validation", error.message).exec()
                continue

        self._wait_condition.wakeOne()
        self.extract_worker.receive_data = Path(super_map_path)

    def _toggle_control_element_enable(self, state: bool):
        self.main_window.btn_extract.setEnabled(state)
        self.main_window.combobox_cpu_type.setEnabled(state)
        self.main_window.tool_btn_input_path.setEnabled(state)
        self.main_window.tool_btn_output_path.setEnabled(state)
        self.main_window.input_path.setEnabled(state)
        self.main_window.output_path.setEnabled(state)

    def _update_log_view(self, message: LogMessageModel):
        self._messages.append(message)
        self.main_window.log.append(self._log_renders["one"].render(LogLevel=LogLevel, dark_mode=self._themas.is_dark, **message.__dict__))

    def _update_style_log(self):
        if not self._messages:
            return

        self.main_window.log.clear()
        log_records = {
            "LogLevel": LogLevel,
            "dark_mode": self._themas.is_dark,
            "records": [{**item.__dict__} for item in self._messages]
        }
        self.main_window.log.append(self._log_renders["many"].render(**log_records))

    def init(self, **kwargs):
        cpu_type = kwargs.get("cpu", None)
        input_file = kwargs.get("input_file", None)
        output_dir = kwargs.get("output_dir", None)

        if cpu_type:
            find_index = [i for i in range(self.main_window.combobox_cpu_type.count()) if
                          self.main_window.combobox_cpu_type.itemText(i).lower() == cpu_type.lower()][0]
            self.main_window.combobox_cpu_type.setCurrentIndex(find_index)

        if input_file:
            self.main_window.input_path.setText(str(input_file))

        if output_dir:
            self.main_window.output_path.setText(str(output_dir))

    def run(self):
        input_file = Path(self.main_window.input_path.text())
        output_dir = Path(self.main_window.output_path.text())
        extractor_name = f"{input_file.suffix[1:]}_{self.main_window.combobox_cpu_type.currentText().lower()}"
        payload = PayloadModel(input_file=input_file, output_dir=output_dir)
        self.main_window.log.clear()
        self._messages.clear()
        self._toggle_control_element_enable(False)

        self.extract_worker.start.emit(extractor_name, payload, self._mutex, self._wait_condition)
