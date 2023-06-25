from pathlib import Path
from typing import BinaryIO

from core.interfaces import ILogService
from core.models import PayloadModel
from extractors.BaseExtractor import BaseExtractor

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class SuperImgExtractor(BaseExtractor):
    def __init__(self, logger: ILogService):
        super().__init__(logger)

    def extract(self, fd: BinaryIO, output_dir: Path, file_size) -> PayloadModel:
        pass

    def run(self, payload: PayloadModel) -> PayloadModel:
        self.logger.error("Not implemented")
        return payload
