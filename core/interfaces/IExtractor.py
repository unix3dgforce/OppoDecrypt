import abc
from pathlib import Path
from typing import BinaryIO

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class IExtractor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, fd: BinaryIO, output_dir: Path, file_size) -> None:
        """Starting the extraction process"""

    @abc.abstractmethod
    def extract(self, input_file: Path, output_dir: Path) -> None:
        """Abstract method extract"""
