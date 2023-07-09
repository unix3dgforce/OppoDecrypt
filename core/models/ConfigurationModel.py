import dataclasses
from typing import Any

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


@dataclasses.dataclass
class ConfigurationModel:
    value: Any
    name: str
    selected: bool = False

