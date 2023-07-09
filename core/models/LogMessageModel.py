import dataclasses
from datetime import datetime

from core.models import LogLevel

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


@dataclasses.dataclass
class LogMessageModel:
    level: LogLevel
    text: str
    time: datetime
