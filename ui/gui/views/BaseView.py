import abc
from PyQt6.QtGui import QFont

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


class BaseView(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def setup(self) -> None:
        """ Setup """

    @abc.abstractmethod
    def translate(self) -> None:
        """ Translation UI """

    @classmethod
    def set_font(cls, *, size: int = 10, bold: bool = False, weight: int = 50) -> QFont:
        font = QFont()
        font.setPointSize(size)
        font.setBold(bold)
        font.setWeight(weight)
        return font
