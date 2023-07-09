from pathlib import Path
from typing import TypeVar

from PyQt6.QtCore import QWaitCondition, pyqtSignal, QObject, QMutex

from core.interfaces import IUserInterface, IExtractor, ILogService
from core.models import PayloadModel, ConfigurationModel, LogMessageModel, LogLevel
from core.models.super import MetadataPartitionModel
from core.utils import Utils
from exceptions import MtkExtractorUnsupportedCryptoSettingsError, QualcommExtractorUnsupportedCryptoSettingsError, \
    QualcommExtractorXMLSectionNotFoundError

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


T = TypeVar('T')


class ExtractWorker(IUserInterface, QObject):
    start = pyqtSignal(str, PayloadModel, QMutex, QWaitCondition)
    finished = pyqtSignal()
    ask_continue_execution_question = pyqtSignal(str)
    ask_extract_partitions_folder = pyqtSignal(Path)
    ask_super_map_path = pyqtSignal(list, Path)
    ask_configuration = pyqtSignal(list)
    ask_partition = pyqtSignal(list)
    log_updated = pyqtSignal(LogMessageModel)

    def __init__(self, extractors: dict[str, IExtractor], logger: ILogService):
        super().__init__()
        self._logger = logger
        self._logger.add_logger_sink(self._update_log)
        self._mutex: QMutex | None = None
        self._wait_condition: QWaitCondition | None = None
        for item in extractors.values():
            item.user_interface = self

        self._extractors = extractors
        self._data: T = None

    def _get_extractors_chain(self, key: str) -> IExtractor:
        _extractor = self._extractors.get(key)
        _extractor.set_next_extractor(self._extractors.get("sparse")).set_next_extractor(self._extractors.get("super"))
        return _extractor

    def _update_log(self, message):
        record = message.record
        self.log_updated.emit(LogMessageModel(level=LogLevel(record["level"].no), text=record["message"], time=record["time"]))

    @property
    def receive_data(self) -> T:
        return self._data

    @receive_data.setter
    def receive_data(self, data: T) -> None:
        self._data = data

    def choice_build_configuration(self, input_files: list[Path], default_path: Path) -> list[Path]:
        csv_records = Utils.parse_csv_file(self.get_super_map_path(input_files, default_path))

        self._mutex.lock()
        self.ask_configuration.emit(
            [ConfigurationModel(
                value=[item for item in input_files if item.name in record.images],
                name=f"[0x{record.id:02X}] {record.name}",
                selected=False
            )for record in csv_records]
        )
        self._wait_condition.wait(self._mutex)
        self._mutex.unlock()

        if isinstance(self._data, list):
            return self._data

    def choice_extraction_partitions(self, partitions: list[MetadataPartitionModel]) -> list[MetadataPartitionModel]:
        self._mutex.lock()
        self.ask_partition.emit(partitions)
        self._wait_condition.wait(self._mutex)
        self._mutex.unlock()

        if isinstance(self._data, list):
            return self._data

    def get_super_map_path(self, input_files: list[Path], default_path: Path) -> Path:
        self._mutex.lock()
        self.ask_super_map_path.emit(input_files, default_path)
        self._wait_condition.wait(self._mutex)
        self._mutex.unlock()

        if isinstance(self._data, Path):
            return self._data

    def get_custom_extract_folder(self, output_folder: Path) -> Path:
        self._mutex.lock()
        self.ask_extract_partitions_folder.emit(output_folder)
        self._wait_condition.wait(self._mutex)
        self._mutex.unlock()

        if isinstance(self._data, Path):
            return self._data

        return output_folder

    def launch_confirmation(self, message: str, payload: PayloadModel, forced: bool = False) -> bool:
        if payload.input_file is None or forced:
            self._mutex.lock()
            self.ask_continue_execution_question.emit(message)
            self._wait_condition.wait(self._mutex)
            self._mutex.unlock()

            if isinstance(self._data, bool):
                return self._data
        else:
            return True

    def run(self, extractor_name: str, payload: PayloadModel, mutex: QMutex, wait_condition: QWaitCondition):
        self._mutex = mutex
        self._wait_condition = wait_condition
        try:
            self._get_extractors_chain(extractor_name).run(payload)
        except (QualcommExtractorUnsupportedCryptoSettingsError,
                QualcommExtractorXMLSectionNotFoundError,
                MtkExtractorUnsupportedCryptoSettingsError) as error:
            self._logger.error(error.message)

        except PermissionError as error:
            self._logger.critical(f'{error.strerror}. {error.filename}')

        finally:
            self._logger.information(f"Extracted complete!")
            self.finished.emit()
