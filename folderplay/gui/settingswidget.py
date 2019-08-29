import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QCheckBox,
    QGroupBox,
    QFileDialog,
    QSizePolicy,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
)

from folderplay.constants import NOT_AVAILABLE
from folderplay.gui.button import ScalablePushButton
from folderplay.gui.label import ElidedLabel
from folderplay.utils import resource_path, is_windows, is_macos, is_linux


class SettingsWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Search box
        self.txt_search_box = QLineEdit(self)
        self.setup_search_line_edit()

        self.chk_hide_watched = QCheckBox(self)
        self.setup_hide_watched_checkbox()

        self.chk_regex = QCheckBox(self)
        self.setup_regex_checkbox()

        self.grp_filters = QGroupBox(self)
        self.setup_filter_group_box()

        # Local player box
        self.grp_selected_player = QGroupBox(self)
        self.setup_local_player_group_box()

        self.lbl_player = ElidedLabel(self)
        self.setup_player_label()

        self.lbl_player_name = ElidedLabel(self)
        self.setup_player_name_label()

        self.btn_change_player = ScalablePushButton(self)
        self.setup_change_player_button()

        self.dlg_select_player = QFileDialog(self)
        self.setup_player_open_dialog()

        self.setLayout(self.get_layout())
        self.layout().setContentsMargins(0, 0, 0, 0)

    def get_layout(self):
        final_layout = QVBoxLayout()
        filter_box_layout = QVBoxLayout()
        player_box_layout = QHBoxLayout()

        checkboxes_layout = QHBoxLayout()
        checkboxes = [self.chk_hide_watched, self.chk_regex]
        for w in checkboxes:
            checkboxes_layout.addWidget(w)

        player_labels = [
            self.lbl_player,
            self.lbl_player_name,
            self.btn_change_player,
        ]
        for w in player_labels:
            player_box_layout.addWidget(w)

        self.grp_selected_player.setLayout(player_box_layout)

        filter_box_layout.addLayout(checkboxes_layout)
        filter_box_layout.addWidget(self.txt_search_box)

        self.grp_filters.setLayout(filter_box_layout)

        final_layout.addWidget(self.grp_selected_player)
        final_layout.addWidget(self.grp_filters)

        return final_layout

    def setup_local_player_group_box(self):
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.grp_selected_player.setSizePolicy(size_policy)
        self.grp_selected_player.setTitle("Player")

    def setup_search_line_edit(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.txt_search_box.setSizePolicy(size_policy)
        self.txt_search_box.setPlaceholderText("Search...")

    def setup_hide_watched_checkbox(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chk_hide_watched.setSizePolicy(size_policy)
        self.chk_hide_watched.setText("Hide watched")

    def setup_regex_checkbox(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chk_regex.setSizePolicy(size_policy)
        self.chk_regex.setText("Regex")

    def setup_filter_group_box(self):
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.grp_filters.setSizePolicy(size_policy)
        self.grp_filters.setTitle("Filter")

    def setup_player_label(self):
        self.lbl_player.setText("Name:")

    def setup_player_name_label(self):
        self.lbl_player_name.setText(NOT_AVAILABLE)

    def setup_change_player_button(self):
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.btn_change_player.setSizePolicy(size_policy)
        self.btn_change_player.setToolTip("Change player")
        self.btn_change_player.setIcon(
            QIcon(resource_path("assets/icons/folder_open.svg"))
        )

    def setup_player_open_dialog(self):
        directory = None
        if is_linux():
            directory = "/usr/bin"
        elif is_windows():
            directory = os.getenv("ProgramFiles(x86)")
            self.dlg_select_player.setNameFilter("Executable Files (*.exe)")
        elif is_macos():
            directory = "/Applications"

        self.dlg_select_player.setWindowTitle("Select new player")
        self.dlg_select_player.setWindowIcon(
            QIcon(resource_path("assets/icons/icon.ico"))
        )
        self.dlg_select_player.setDirectory(directory)
        self.dlg_select_player.setMinimumSize(QApplication.desktop().size() / 2)
        self.dlg_select_player.setFileMode(QFileDialog.ExistingFile)
        self.dlg_select_player.setViewMode(QFileDialog.Detail)
        self.dlg_select_player.setAcceptMode(QFileDialog.AcceptOpen)
        self.dlg_select_player.setOptions(
            QFileDialog.DontUseNativeDialog
            | QFileDialog.ReadOnly
            | QFileDialog.HideNameFilterDetails
        )
        # self.dlg_select_player.setFilter(QDir.Executable)
        self.dlg_select_player.adjustSize()
