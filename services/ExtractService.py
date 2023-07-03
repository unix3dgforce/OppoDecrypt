import asyncio
import sys

from qasync import QEventLoop

from core.interfaces import IExtractor, IBaseExtractService, ILogService, IUserInterface
from core.models import PayloadModel
from core.utils import ExitCode
from exceptions import QualcommExtractorUnsupportedCryptoSettingsError, QualcommExtractorXMLSectionNotFoundError, \
    MtkExtractorUnsupportedCryptoSettingsError

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class ExtractService(IBaseExtractService):
    def __init__(self, extractors: dict[str, IExtractor], user_interfaces: dict[str: IUserInterface], logger: ILogService):
        self._extractors = extractors
        self._user_interfaces = user_interfaces
        self._logger = logger

    def _extract_with_gui(self, user_interface: IUserInterface, **kwargs):
        user_interface.extractors = self._extractors
        loop = QEventLoop(user_interface.app)
        asyncio.set_event_loop(loop)

        user_interface.show()

        with loop:
            loop.run_forever()

        sys.exit(ExitCode.OK)

    def _extract_with_cli(self, user_interface: IUserInterface, **kwargs):
        self._set_extractors_user_interface(user_interface)

        try:
            if not (cpu := kwargs.pop('cpu', None)):
                self._logger.error(f"Unsupported cpu type")
                sys.exit(ExitCode.USAGE)

            prefix = kwargs.get("input_file").suffix[1:]

            extractor = self._extractors[f"{prefix}_{cpu}"]
            if kwargs.pop("sparse"):
                extractor.set_next_extractor(self._extractors.get("sparse")).set_next_extractor(self._extractors.get("super"))

            extractor.run(PayloadModel(**kwargs))

        except (QualcommExtractorUnsupportedCryptoSettingsError,
                QualcommExtractorXMLSectionNotFoundError,
                MtkExtractorUnsupportedCryptoSettingsError) as error:
            self._logger.error(error.message)

        except KeyError:
            self._logger.error(f"Not found extractor")

        except PermissionError as error:
            self._logger.critical(f'{error.strerror}. {error.filename}')

        except KeyboardInterrupt:
            self._logger.critical(f"Oooopss....  program terminated")

    def _set_extractors_user_interface(self, user_interface: IUserInterface):
        for item in self._extractors.values():
            item.user_interface = user_interface

    def extract(self, **kwargs) -> None:
        if kwargs.pop("gui", False):
            user_interface = self._user_interfaces.get("gui")
            self._extract_with_gui(user_interface, **kwargs)
        else:
            user_interface = self._user_interfaces.get("cli")
            self._extract_with_cli(user_interface, **kwargs)
