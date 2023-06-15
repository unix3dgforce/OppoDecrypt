from dependency_injector import containers, providers
from services import ExtractService, LoguruLoggingService
from extractors import QualcommExtractor, MtkExtractor
from core.models import CpuSupportEnum

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class ApplicationContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration()

    logging = providers.Singleton(
        LoguruLoggingService,
        configuration=configuration.log
    )

    extract_service = providers.Factory(
        ExtractService,
        extractors=providers.Dict({
            CpuSupportEnum.QC: providers.Factory(
                QualcommExtractor,
                configuration=configuration.extractors.ofp_qualcomm,
                logger=logging
            ),
            CpuSupportEnum.MTK: providers.Factory(
                MtkExtractor,
                configuration=configuration.extractors.ofp_mtk,
                logger=logging
            ),

        }),
        logger=logging
    )
