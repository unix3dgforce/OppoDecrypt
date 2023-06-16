import shutil
from pathlib import Path
from typing import BinaryIO

from core.interfaces import IExtractor, ILogService

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class OpsExtractor(IExtractor):
    def __init__(self, configuration: dict[str, any], logger: ILogService):
        self._logger = logger

    def _extract(self, fd: BinaryIO, output_dir: Path, file_size):
        self._logger.critical("Not implemented")

    def extract(self, input_file: Path, output_dir: Path) -> None:
        self._logger.information("Run OPS extractors")

        if output_dir.exists():
            shutil.rmtree(output_dir)

        output_dir.mkdir(parents=True)
        file_size = input_file.stat().st_size

        with open(input_file, 'rb') as fd:
            self._extract(fd, output_dir, file_size)

        self._logger.information(f'Extract successfully')
