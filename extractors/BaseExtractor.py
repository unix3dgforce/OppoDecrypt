import abc
import shutil
from pathlib import Path
from typing import BinaryIO

from core.interfaces import IExtractor, ILogService
from core.models import CryptoCredential

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class BaseExtractor(IExtractor):
    def __init__(self, logger: ILogService):
        self.crypto_config: CryptoCredential | None = None
        self.logger = logger

    def run(self, fd: BinaryIO, output_dir: Path, file_size) -> None:
        ...

    def extract(self, input_file: Path, output_dir: Path) -> None:
        if output_dir.exists():
            shutil.rmtree(output_dir)

        output_dir.mkdir(parents=True)
        file_size = input_file.stat().st_size

        with open(input_file, 'rb') as fd:
            self.run(fd, output_dir, file_size)

        self.logger.information(f'Extract successfully')
