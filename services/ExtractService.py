import sys

from core.interfaces import IExtractor, IBaseExtractService, ILogService
from core.models import CpuSupportEnum
from core.utils import ExitCode
from exceptions import QualcommExtractorUnsupportedCryptoSettingsError, QualcommExtractorXMLSectionNotFoundError

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class ExtractService(IBaseExtractService):
    def __init__(self, extractors: dict[CpuSupportEnum, IExtractor], logger: ILogService):
        self._extractors = extractors
        self._logger = logger

    def extract(self, **kwargs) -> None:
        try:
            if not (cpu := kwargs.pop('cpu', None)):
                self._logger.error(f"Unsupported cpu type")
                sys.exit(ExitCode.USAGE)

            self._extractors[cpu].extract(**kwargs)
        except (QualcommExtractorUnsupportedCryptoSettingsError, QualcommExtractorXMLSectionNotFoundError) as error:
            self._logger.error(error.message)

        except KeyError:
            self._logger.error(f"Not found extractor")
