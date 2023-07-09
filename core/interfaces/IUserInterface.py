import abc
from pathlib import Path

from core.models import PayloadModel, CsvRecordModel
from core.models.super import MetadataPartitionModel

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class IUserInterface:

    @abc.abstractmethod
    def choice_build_configuration(self, input_files: list[Path], default_path: Path) -> list[Path]:
        """ Get build configuration """

    @abc.abstractmethod
    def choice_extraction_partitions(self, partitions: list[MetadataPartitionModel]) -> list[MetadataPartitionModel]:
        """ Get list extract partitions """

    @abc.abstractmethod
    def get_super_map_path(self, input_files: list[Path], default_path: Path) -> Path:
        """ Get path to super_map.csv file """

    @abc.abstractmethod
    def get_custom_extract_folder(self, output_folder: Path) -> Path:
        """ Get extract folder path """

    @abc.abstractmethod
    def launch_confirmation(self, message: str, payload: PayloadModel, forced: bool = False) -> bool:
        """ Confirmation launch """
