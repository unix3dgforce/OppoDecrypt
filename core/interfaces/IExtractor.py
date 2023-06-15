import abc
from pathlib import Path

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class IExtractor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def extract(self, input_file: Path, output_dir: Path) -> None:
        """Abstract method extract"""
