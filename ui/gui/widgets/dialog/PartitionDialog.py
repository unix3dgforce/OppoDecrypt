from PyQt6 import QtCore, QtGui, QtWidgets

from .ChoiceDialog import ChoiceDialog

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


class PartitionDialog(ChoiceDialog):
    def setup_ui(self) -> None:
        self.resize(200, 200)
        self.setWindowFlags(self.windowFlags() &
                            ~QtCore.Qt.WindowType.WindowContextHelpButtonHint &
                            ~QtCore.Qt.WindowType.WindowCloseButtonHint)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/gui/resources/main.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        size_policy_wdget = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        size_policy_wdget.setHorizontalStretch(0)
        size_policy_wdget.setVerticalStretch(0)
        size_policy_wdget.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(size_policy_wdget)

        widget_vertical_layout = QtWidgets.QVBoxLayout(self)
        widget_vertical_layout.setObjectName("widget_vertical_layout")
        widget_vertical_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)
        widget_vertical_layout.setContentsMargins(10, 10, 10, 10)

        partition_group_box = QtWidgets.QGroupBox(self)
        partition_group_box.setObjectName("partitions_group_box")
        partition_group_box.setTitle("Partitions")

        size_policy_group_box = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        size_policy_group_box.setHorizontalStretch(0)
        size_policy_group_box.setVerticalStretch(0)
        size_policy_group_box.setHeightForWidth(partition_group_box.hasHeightForWidth())
        partition_group_box.setSizePolicy(size_policy_group_box)

        configuration_group_box_vertical_layout = QtWidgets.QVBoxLayout(partition_group_box)
        configuration_group_box_vertical_layout.setObjectName("partition_group_box_vertical_layout")
        configuration_group_box_vertical_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setObjectName("grid_layout")
        grid_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)

        check_box_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        check_box_size_policy.setHorizontalStretch(0)
        check_box_size_policy.setVerticalStretch(0)

        button_box = QtWidgets.QDialogButtonBox(self)
        button_box.setObjectName("button_box")
        button_box_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        button_box_size_policy.setHorizontalStretch(0)
        button_box_size_policy.setVerticalStretch(0)
        button_box_size_policy.setHeightForWidth(button_box.sizePolicy().hasHeightForWidth())
        button_box.setSizePolicy(button_box_size_policy)
        button_box.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        button_box.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        button_box.rejected.connect(self.accept)
        button_box.accepted.connect(self.accept)

        select_all_check_box = QtWidgets.QCheckBox(self)
        select_all_check_box.setObjectName("select_all_check_box")
        select_all_check_box.setText("Select All")
        select_all_check_box.setChecked(True)
        select_all_check_box.clicked.connect(self._toggle_select_all)

        filtered_items = [item for item in self.items if item.num_extents != 0]

        for index, (row, col, row_span, col_span) in enumerate(self.generate_grid(filtered_items)):
            cb = QtWidgets.QCheckBox(partition_group_box)
            cb.setChecked(True)
            cb.setText(filtered_items[index].name[:-2])
            cb.setObjectName(filtered_items[index].name)
            cb.setGeometry(QtCore.QRect(5, 90, 90, 20))
            cb.stateChanged.connect(lambda: self.findChild(QtWidgets.QCheckBox, "select_all_check_box").setChecked(False))
            check_box_size_policy.setHeightForWidth(cb.sizePolicy().hasHeightForWidth())
            cb.setSizePolicy(check_box_size_policy)
            grid_layout.addWidget(cb, row, col, 1, 1)

        configuration_group_box_vertical_layout.addLayout(grid_layout)
        widget_vertical_layout.addWidget(partition_group_box)
        widget_vertical_layout.addWidget(select_all_check_box)
        widget_vertical_layout.addWidget(button_box)

    def _set_state(self, state: bool):
        for check_box in [item for item in self.findChildren(QtWidgets.QCheckBox)]:
            check_box.setChecked(state)

    def _toggle_select_all(self):
        if self.sender().isChecked():
            self._set_state(True)
        else:
            self._set_state(False)

    def accept(self) -> None:
        if (select_all_check_box := self.findChild(QtWidgets.QCheckBox, "select_all_check_box")).isChecked():
            self.choice = self.items
            self.close()

        check_boxes = [item for item in self.findChildren(QtWidgets.QCheckBox) if item != select_all_check_box and item.isChecked()]
        self.choice = [self.items_dict.get(item.objectName()) for item in check_boxes]
        self.close()

    @classmethod
    def getPartitions(cls, title: str, items: list, count_colum: int, parent=None):
        dialog = PartitionDialog(title, items, count_colum, parent)
        while dialog.exec() == 0:
            if not dialog.choice:
                continue
            break

        return dialog.choice

