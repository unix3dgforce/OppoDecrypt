from pathlib import Path
from typing import BinaryIO

from .BaseExtractor import BaseExtractor
from core.interfaces import ILogService

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class OpsExtractor(BaseExtractor):
    def __init__(self, configuration: dict[str, any], logger: ILogService):
        super().__init__(logger)

    def run(self, fd: BinaryIO, output_dir: Path, file_size):
        self.logger.critical("Not implemented")

    def extract(self, input_file: Path, output_dir: Path) -> None:
        self.logger.information("Run OPS extractor")

        super().extract(input_file, output_dir)
