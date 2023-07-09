from .ChoiceDialog import ChoiceDialog
from PyQt6 import QtWidgets, QtCore, QtGui

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


class ConfigurationDialog(ChoiceDialog):
    def setup_ui(self):
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

        configuration_group_box = QtWidgets.QGroupBox(self)
        configuration_group_box.setObjectName("configurations_group_box")
        configuration_group_box.setTitle("Configurations")

        size_policy_group_box = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        size_policy_group_box.setHorizontalStretch(0)
        size_policy_group_box.setVerticalStretch(0)
        size_policy_group_box.setHeightForWidth(configuration_group_box.hasHeightForWidth())
        configuration_group_box.setSizePolicy(size_policy_group_box)

        configuration_group_box_vertical_layout = QtWidgets.QVBoxLayout(configuration_group_box)
        configuration_group_box_vertical_layout.setObjectName("configuration_group_box_vertical_layout")
        configuration_group_box_vertical_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setObjectName("grid_layout")
        grid_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)

        radio_button_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        radio_button_size_policy.setHorizontalStretch(0)
        radio_button_size_policy.setVerticalStretch(0)

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

        for index, (row, col, row_span, col_span) in enumerate(self.generate_grid(self.items)):
            rb = QtWidgets.QRadioButton(configuration_group_box)
            rb.setText(self.items[index].name)
            rb.setChecked(self.items[index].selected)
            rb.setObjectName(f"rb_{index}")
            rb.setGeometry(QtCore.QRect(5, 90, 90, 20))
            radio_button_size_policy.setHeightForWidth(rb.sizePolicy().hasHeightForWidth())
            rb.setSizePolicy(radio_button_size_policy)
            grid_layout.addWidget(rb, row, col, 1, 1)

        configuration_group_box_vertical_layout.addLayout(grid_layout)
        widget_vertical_layout.addWidget(configuration_group_box)
        widget_vertical_layout.addWidget(button_box)

    def accept(self) -> None:
        if not (result := [rb for rb in self.findChildren(QtWidgets.QRadioButton) if rb.isChecked()]):
            return

        self.choice = self.items_dict.get(result[0].text()).value
        self.close()

    @classmethod
    def getConfigurations(cls, title: str, items: list, count_colum: int, parent=None):
        dialog = ConfigurationDialog(title, items, count_colum, parent)
        while dialog.exec() == 0:
            if not dialog.choice:
                continue
            break

        return dialog.choice
