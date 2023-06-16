from dependency_injector import containers, providers
from services import ExtractService, LoguruLoggingService
from extractors import OfpQualcommExtractor, MtkExtractor
from core.models import CpuSupportEnum

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'

OFP_PREFIX = "ofp"
OSP_PREFIX = "ops"


class ApplicationContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration()

    logging = providers.Singleton(
        LoguruLoggingService,
        configuration=configuration.log
    )

    extract_service = providers.Factory(
        ExtractService,
        extractors=providers.Dict({
            f"{OFP_PREFIX}_{CpuSupportEnum.QC.value}": providers.Factory(
                OfpQualcommExtractor,
                configuration=configuration.extractors.ofp_qualcomm,
                logger=logging
            ),
            f"{OFP_PREFIX}_{CpuSupportEnum.MTK.value}": providers.Factory(
                MtkExtractor,
                configuration=configuration.extractors.ofp_mtk,
                logger=logging
            ),

        }),
        logger=logging
    )
