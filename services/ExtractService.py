from core.interfaces import IExtractor, IBaseExtractService, ILogService
from core.models import ExtractorEnum
from exceptions import QualcommExtractorUnsupportedCryptoSettingsError, QualcommExtractorXMLSectionNotFoundError

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class ExtractService(IBaseExtractService):
    def __init__(self, extractors: dict[ExtractorEnum, IExtractor], logger: ILogService):
        self._extractors = extractors
        self._logger = logger

    def extract(self, **kwargs) -> None:
        try:
            self._extractors[ExtractorEnum.OFP_QUALCOMM].extract(**kwargs)
        except (QualcommExtractorUnsupportedCryptoSettingsError, QualcommExtractorXMLSectionNotFoundError) as error:
            self._logger.error(error.message)
