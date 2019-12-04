import os

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
    QFrame,
    QComboBox,
)

from folderplay.constants import NOT_AVAILABLE
from folderplay.gui.button import ScalablePushButton
from folderplay.gui.icons import IconSet, main_icon
from folderplay.gui.label import ElidedLabel, NameLabel
from folderplay.gui.styles import Style
from folderplay.utils import is_windows, is_macos, is_linux


class SettingsWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Search box
        self.txt_search_box = QLineEdit(self)
        self.setup_search_line_edit()

        # Hide watched checkbox
        self.chk_hide_watched = QCheckBox(self)
        self.setup_hide_watched_checkbox()

        # Regex checkbox
        self.chk_regex = QCheckBox(self)
        self.setup_regex_checkbox()

        self.chk_rename = QCheckBox(self)
        self.setup_rename_checkbox()

        # Settings groupbox
        self.grp_settings = QGroupBox(self)
        self.setup_settings_group_box()

        # Player settings
        self.lbl_player = NameLabel(self)
        self.setup_player_label()

        self.lbl_player_name = ElidedLabel(self)
        self.setup_player_name_label()

        self.btn_change_player = ScalablePushButton(self)
        self.setup_change_player_button()

        self.dlg_select_player = QFileDialog(self)
        self.setup_player_open_dialog()

        # Style combobox
        self.cmb_style = QComboBox(self)
        self.lbl_combo_style = NameLabel(self)
        self.setup_style_combobox()

        self.cmb_icon = QComboBox(self)
        self.lbl_combo_icon = NameLabel(self)
        self.setup_icon_combobox()

        self.setLayout(self.get_layout())
        self.layout().setContentsMargins(0, 0, 0, 0)

    def create_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def get_layout(self):
        vl_final = QVBoxLayout()
        vl_filter = QVBoxLayout()
        hl_player = QHBoxLayout()

        hl_checkboxes = QHBoxLayout()
        checkboxes = [self.chk_hide_watched, self.chk_regex, self.chk_rename]
        for w in checkboxes:
            hl_checkboxes.addWidget(w)

        player_labels = [
            self.lbl_player,
            self.lbl_player_name,
            self.btn_change_player,
        ]
        for w in player_labels:
            hl_player.addWidget(w)

        hl_comboboxes = QHBoxLayout()
        combos = [
            self.lbl_combo_style,
            self.cmb_style,
            self.lbl_combo_icon,
            self.cmb_icon,
        ]
        for w in combos:
            hl_comboboxes.addWidget(w)

        vl_filter.addLayout(hl_comboboxes)
        vl_filter.addWidget(self.create_line())
        vl_filter.addLayout(hl_player)
        vl_filter.addWidget(self.create_line())
        vl_filter.addLayout(hl_checkboxes)
        vl_filter.addWidget(self.txt_search_box)

        self.grp_settings.setLayout(vl_filter)

        vl_final.addWidget(self.grp_settings)

        return vl_final

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

    def setup_rename_checkbox(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chk_rename.setSizePolicy(size_policy)
        self.chk_rename.setText("Rename")
        self.chk_rename.setToolTip("Rename media titles according to regex")

    def setup_settings_group_box(self):
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.grp_settings.setSizePolicy(size_policy)
        self.grp_settings.setTitle("Settings")

    def setup_player_label(self):
        self.lbl_player.setText("Player:")

    def setup_player_name_label(self):
        self.lbl_player_name.setText(NOT_AVAILABLE)

    def setup_change_player_button(self):
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.btn_change_player.setSizePolicy(size_policy)
        self.btn_change_player.setToolTip("Change player")
        self.btn_change_player.setIcon(IconSet.current.folder_open)

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
        self.dlg_select_player.setWindowIcon(main_icon())
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
        self.dlg_select_player.adjustSize()

    def setup_style_combobox(self):
        self.lbl_combo_style.setText("Style:")
        styles = [x.capitalize() for x in Style.names()]
        self.cmb_style.addItems(styles)

    def setup_icon_combobox(self):
        self.lbl_combo_icon.setText("Icons:")
        for iconset in IconSet:
            self.cmb_icon.addItem(iconset.value.play, iconset.name.capitalize())
