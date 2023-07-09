import abc
import math
import typing

from PyQt6 import QtWidgets, QtCore

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"

T = typing.TypeVar('T')


class ChoiceDialog(QtWidgets.QDialog):
    _choice_result = []

    def __init__(self, title: str, items: list[T], count_colum: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.items = items
        self.items_dict = {item.name: item for item in items}
        self.count_colum = count_colum
        self.row_limit = math.ceil(len(items) / count_colum)
        self.setup_ui()

    @abc.abstractmethod
    def setup_ui(self) -> None:
        """ Setup ui """

    @property
    def choice(self) -> list[T]:
        return self._choice_result

    @choice.setter
    def choice(self, value: list[T]) -> None:
        self._choice_result = value

    def generate_grid(self, items) -> list[tuple[int, int, int, QtCore.Qt.AlignmentFlag]]:
        self.row_limit = math.ceil(len(items) / self.count_colum)
        result = []
        colum_counter = 0
        for row_index in range(0, len(items)):
            if row_index > self.row_limit:
                row_index -= self.row_limit

            if row_index == self.row_limit:
                row_index = 0
                colum_counter += 1

            result.append((row_index, colum_counter, 1, QtCore.Qt.AlignmentFlag.AlignLeft))

        return result

