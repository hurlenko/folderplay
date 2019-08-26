import os

from PyQt5.QtCore import QSize, Qt, QEventLoop
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow,
    QListWidget,
    QLineEdit,
    QCheckBox,
    QGroupBox,
    QFileDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
    QSizePolicy,
    QAbstractItemView,
    QLayout)

from folderplay.constants import MAX_MOVIE_TITLE_LENGTH, NOT_AVAILABLE
from folderplay.gui.basicview import BasicViewWidget
from folderplay.gui.button import ScalablePushButton
from folderplay.gui.label import ElidedLabel
from folderplay.utils import resource_path, is_linux, is_windows, is_macos


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        average_char_width = self.fontMetrics().averageCharWidth()
        self.advanced_view_size = 1600
        self.basic_view_size = average_char_width * (MAX_MOVIE_TITLE_LENGTH + 5)

        self.basic_view_widget = BasicViewWidget(self)
        self.basic_view_widget.btn_advanced.clicked.connect(
            self.toggle_advanced_view
        )
        self.basic_view_widget.setFixedWidth(self.basic_view_size)

        # File names list view
        self.lst_files = QListWidget()
        self.setup_files_list()

        # Search box
        self.txt_search_box = QLineEdit()
        self.setup_search_line_edit()

        self.chk_hide_watched = QCheckBox()
        self.setup_hide_watched_checkbox()

        self.chk_regex = QCheckBox()
        self.setup_regex_checkbox()

        self.grp_filters = QGroupBox()
        self.setup_filter_group_box()

        # Local player box
        self.grp_selected_player = QGroupBox()
        self.setup_local_player_group_box()

        self.lbl_player = ElidedLabel()
        self.setup_player_label()

        self.lbl_player_name = ElidedLabel()
        self.setup_player_name_label()

        self.btn_change_player = ScalablePushButton()
        self.setup_change_player_button()

        self.dlg_select_player = QFileDialog()
        self.setup_player_open_dialog()

        self.advanced_view_widgets = [
            self.lst_files,
            self.txt_search_box,
            self.chk_hide_watched,
            self.chk_hide_watched,
            self.chk_regex,
            self.grp_filters,
            self.grp_selected_player,
            self.lbl_player,
            self.lbl_player_name,
        ]

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main window
        self.setup_main_window()

    def advanced_view_layout(self):
        vlayout_left_pane = QVBoxLayout()
        vlayout_group_box = QVBoxLayout()
        hlayout = QHBoxLayout()

        hlayout_checkboxes = QHBoxLayout()
        checkboxes = [self.chk_hide_watched, self.chk_regex]
        for w in checkboxes:
            hlayout_checkboxes.addWidget(w)

        hlayout_player_labels = QHBoxLayout()
        player_labels = [
            self.lbl_player,
            self.lbl_player_name,
            self.btn_change_player,
        ]
        for w in player_labels:
            hlayout_player_labels.addWidget(w)

        self.grp_selected_player.setLayout(hlayout_player_labels)

        vlayout_group_box.addLayout(hlayout_checkboxes)
        vlayout_group_box.addWidget(self.txt_search_box)

        self.grp_filters.setLayout(vlayout_group_box)

        vlayout_left_pane.addWidget(self.basic_view_widget)
        vlayout_left_pane.addWidget(self.grp_selected_player)
        vlayout_left_pane.addWidget(self.grp_filters)

        hlayout.addLayout(vlayout_left_pane)
        hlayout.addWidget(self.lst_files)

        return hlayout

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos()
        )
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def toggle_advanced_view(self):
        # QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        if not self.basic_view_widget.btn_advanced.isChecked():
            for w in self.advanced_view_widgets:
                w.hide()
            # self.setFixedWidth(self.basic_view_size)
        else:
            for w in self.advanced_view_widgets:
                w.show()
            # self.setFixedWidth(self.advanced_view_size)

        # Todo fix
        # self.updateGeometry()
        # setSizeConstraint(QLayout::SetFixedSize);
        # https://stackoverflow.com/a/30472749/8014793
        # self.setFixedSize(self.layout().sizeHint())
        # self.resize(self.minimumSizeHint())
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        self.adjustSize()
        # QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        # self.setFixedSize(self.layout().sizeHint())
        self.center()

    # region Widget setup routine
    def setup_main_window(self):
        # size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #
        # self.central_widget.setSizePolicy(size_policy)
        layout = self.advanced_view_layout()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.central_widget.setLayout(layout)
        # self.setFixedSize(self.advanced_view_size)
        self.toggle_advanced_view()

        self.setWindowTitle("FolderPlay by Hurlenko")
        self.setWindowIcon(QIcon(resource_path("assets/icons/icon.ico")))

    def setup_play_button(self):
        # sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # self.btn_play.setSizePolicy(sizePolicy)
        # self.btn_play.setText("Play")
        # font = self.btn_play.font()
        # font.setPointSize(25)
        # font.setBold(True)
        # self.btn_play.setFont(font)
        icon = QIcon(resource_path("assets/icons/play.svg"))
        self.btn_play.setIcon(icon)
        self.btn_play.setIconSize(QSize(100, 100))

    def setup_change_player_button(self):
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.btn_change_player.setSizePolicy(size_policy)
        self.btn_change_player.setToolTip("Change player")
        self.btn_change_player.setIcon(
            QIcon(resource_path("assets/icons/folder_open.svg"))
        )

    def setup_files_list(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lst_files.setSizePolicy(size_policy)
        self.lst_files.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.lst_files.setSortingEnabled(True)
        self.lst_files.setContextMenuPolicy(Qt.CustomContextMenu)

    def setup_search_line_edit(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.txt_search_box.setSizePolicy(size_policy)
        self.txt_search_box.setPlaceholderText("Search...")

    def setup_regex_checkbox(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chk_regex.setSizePolicy(size_policy)
        self.chk_regex.setText("Regex")

    def setup_hide_watched_checkbox(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chk_hide_watched.setSizePolicy(size_policy)
        self.chk_hide_watched.setText("Hide watched")

    def setup_filter_group_box(self):
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.grp_filters.setSizePolicy(size_policy)
        self.grp_filters.setTitle("Filter")

    def setup_local_player_group_box(self):
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.grp_selected_player.setSizePolicy(size_policy)
        self.grp_selected_player.setTitle("Player")

    def setup_player_label(self):
        # size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.lbl_player.setSizePolicy(size_policy)
        self.lbl_player.setText("Name:")

    def setup_player_name_label(self):
        # size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.lbl_player_name.setSizePolicy(size_policy)
        self.lbl_player_name.setText(NOT_AVAILABLE)

    def setup_player_open_dialog(self):
        directory = None
        if is_linux():
            directory = "/usr/bin"
        elif is_windows():
            directory = os.getenv("ProgramFiles")
            self.dlg_select_player.setNameFilter("Executable Files (*.exe)")
        elif is_macos():
            directory = "/usr/bin"

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

    # endregion Widget setup routine
