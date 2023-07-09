from dependency_injector import containers, providers

from ui import Cli
from core.models import CpuSupportEnum
from extractors import OfpQualcommExtractor, MtkExtractor, OpsExtractor, SparseExtractor, SuperImgExtractor
from services import ExtractService, LoguruLoggingService

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'

from ui.gui import App, MainWindow
from ui.gui.workers import ExtractWorker

OFP_PREFIX = "ofp"
OPS_PREFIX = "ops"


class ApplicationContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration()

    logging = providers.Singleton(
        LoguruLoggingService,
        configuration=configuration.log
    )

    app = providers.Singleton(
        App
    )

    extractors = providers.Dict({
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

        f"{OPS_PREFIX}_{CpuSupportEnum.QC.value}": providers.Factory(
            OpsExtractor,
            configuration=configuration.extractors.ops,
            logger=logging
        ),
        f"{OPS_PREFIX}_{CpuSupportEnum.MTK.value}": providers.Factory(
            OpsExtractor,
            configuration=configuration.extractors.ops,
            logger=logging
        ),
        "sparse": providers.Factory(
            SparseExtractor,
            logger=logging
        ),
        "super": providers.Factory(
            SuperImgExtractor,
            logger=logging
        )
    })

    user_interfaces = providers.Dict({
        "cli": providers.Factory(
            Cli
        ),
        "gui": providers.Singleton(
            MainWindow,
            app=app,
            extract_worker=providers.Singleton(
                ExtractWorker,
                extractors=extractors,
                logger=logging
            ),
            configuration=configuration.ui.gui,
            logger=logging
        )
    })

    extract_service = providers.Factory(
        ExtractService,
        extractors=extractors,
        user_interfaces=user_interfaces,
        logger=logging
    )
