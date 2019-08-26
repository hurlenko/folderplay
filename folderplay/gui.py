import os

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QPainter
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
    QSizePolicy,
    QApplication,
    QHBoxLayout,
    QStyle,
    QLineEdit,
    QCheckBox,
    QWidget,
    QAbstractItemView,
    QListWidget,
    QLabel,
    QStyleOptionButton,
    QGroupBox,
    QFileDialog,
)

from folderplay.constants import FONT_SIZE, NOT_AVAILABLE, FINISHED
from folderplay.utils import resource_path, is_linux, is_windows, is_macos


class ScalablePushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pad = 1  # padding between the icon and the button frame
        self.minSize = 8  # minimum size of the icon

        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)
        # self.setStyleSheet("{ padding: 0; margin: 0; }")
        # self.setContentsMargins(0,0,0,0)
        # self.setStyleSheet('QPushButton{margin: 0 0 0 0;}')

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        # get default style
        opt = QStyleOptionButton()
        self.initStyleOption(opt)
        # scale icon to button size
        h = opt.rect.height()
        w = opt.rect.width()
        icon_size = max(min(h, w) - 2 * self.pad, self.minSize)
        opt.iconSize = QSize(icon_size, icon_size)
        # draw button
        self.style().drawControl(QStyle.CE_PushButton, opt, qp, self)
        qp.end()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Play button
        self.btn_play = ScalablePushButton()
        self.setup_play_button()

        # Advanced view button
        self.btn_advanced = ScalablePushButton()
        self.setup_advanced_button()

        self.btn_refresh = ScalablePushButton()
        self.setup_refresh_button()

        # Progressbar
        self.pbr_watched = QProgressBar()
        self.setup_progress_bar()

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

        self.lbl_player = QLabel()
        self.setup_player_label()

        self.lbl_player_name = QLabel()
        self.setup_player_name_label()

        self.btn_change_player = ScalablePushButton()
        self.setup_change_player_button()

        self.dlg_select_player = QFileDialog()
        self.setup_player_open_dialog()

        self.grp_current_media = QGroupBox()
        self.setup_current_media_group_box()

        self.lbl_finishes = QLabel()
        self.setup_finishes_label()
        self.lbl_movie_info = QLabel()
        self.setup_movie_info_label()

        self.lbl_finishes_key = QLabel()
        self.setup_finishes_key_label()
        self.lbl_movie_info_key = QLabel()
        self.setup_movie_info_key_label()

        self.basic_view_widgets = [
            self.btn_play,
            self.btn_advanced,
            self.btn_refresh,
            self.pbr_watched,
            self.lbl_movie_info_key,
            self.lbl_movie_info,
            self.lbl_finishes_key,
            self.lbl_finishes,
            self.grp_current_media,
        ]

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

        self.advanced_view_size = QSize(1600, 600)
        self.basic_view_size = QSize(600, 450)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main window
        self.setup_main_window()

    def basic_view_layout(self):
        vlayout = QVBoxLayout()
        vlayout_refresh_advanced = QVBoxLayout()

        hlayout = QHBoxLayout()

        hlayout_media = QHBoxLayout()
        vlayout_media_left = QVBoxLayout()
        vlayout_media_right = QVBoxLayout()

        widgets = [self.btn_advanced, self.btn_refresh]
        for w in widgets:
            vlayout_refresh_advanced.addWidget(w)

        for w in (self.lbl_finishes_key, self.lbl_movie_info_key):
            vlayout_media_left.addWidget(w)

        for w in (self.lbl_finishes, self.lbl_movie_info):
            vlayout_media_right.addWidget(w)

        hlayout_media.addLayout(vlayout_media_left)
        hlayout_media.addLayout(vlayout_media_right)
        self.grp_current_media.setLayout(hlayout_media)

        hlayout.addWidget(self.pbr_watched)
        hlayout.addLayout(vlayout_refresh_advanced)

        # Button is two times bigger than pbr_watched
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.grp_current_media)
        vlayout.addWidget(self.btn_play)
        return vlayout

    def advanced_view_layout(self):
        vlayout_left_pane = QVBoxLayout()
        vlayout_group_box = QVBoxLayout()
        hlayout = QHBoxLayout()

        basic_layout = self.basic_view_layout()

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

        vlayout_left_pane.addLayout(basic_layout)
        vlayout_left_pane.addWidget(self.grp_selected_player)
        vlayout_left_pane.addWidget(self.grp_filters)

        hlayout.addLayout(vlayout_left_pane, 1)
        hlayout.addWidget(self.lst_files, 2)

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
        # self.adjustSize()

        if not self.btn_advanced.isChecked():
            for w in self.advanced_view_widgets:
                w.hide()
            self.setFixedWidth(self.basic_view_size.width())
        else:
            for w in self.advanced_view_widgets:
                w.show()
            self.setFixedWidth(self.advanced_view_size.width())

        self.adjustSize()
        self.center()

    # region Widget setup routine
    def setup_main_window(self):
        self.central_widget.setLayout(self.advanced_view_layout())
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

    def setup_advanced_button(self):
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.btn_advanced.setSizePolicy(size_policy)
        self.btn_advanced.setToolTip("Advanced options")
        self.btn_advanced.setCheckable(True)
        self.btn_advanced.setIcon(
            QIcon(resource_path("assets/icons/settings.svg"))
        )
        self.btn_advanced.clicked.connect(self.toggle_advanced_view)

    def setup_refresh_button(self):
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.btn_refresh.setSizePolicy(size_policy)
        self.btn_refresh.setToolTip("Refresh")
        self.btn_refresh.setIcon(
            QIcon(resource_path("assets/icons/refresh.svg"))
        )

    def setup_change_player_button(self):
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.btn_change_player.setSizePolicy(size_policy)
        self.btn_change_player.setToolTip("Change player")
        self.btn_change_player.setIcon(
            QIcon(resource_path("assets/icons/folder_open.svg"))
        )

    def setup_progress_bar(self):
        self.pbr_watched.setValue(24)
        # Allow pbr_watched to expand to take up all space in layout
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pbr_watched.setSizePolicy(size_policy)

        self.pbr_watched.setFormat("%v / %m")
        font = self.pbr_watched.font()
        font.setPointSize(25)
        font.setBold(True)
        self.pbr_watched.setFont(font)

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
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.grp_filters.setSizePolicy(size_policy)
        self.grp_filters.setTitle("Filter")

    def setup_local_player_group_box(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.grp_selected_player.setSizePolicy(size_policy)
        self.grp_selected_player.setTitle("Player")

    def setup_player_label(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lbl_player.setSizePolicy(size_policy)
        self.lbl_player.setText("Name:")

    def setup_player_name_label(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lbl_player_name.setSizePolicy(size_policy)
        self.lbl_player_name.setText(NOT_AVAILABLE)

    def setup_current_media_group_box(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.grp_current_media.setSizePolicy(size_policy)
        self.grp_current_media.setTitle(FINISHED)

    def setup_finishes_label(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lbl_finishes.setSizePolicy(size_policy)
        self.lbl_finishes.setText(NOT_AVAILABLE)

    def setup_movie_info_label(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lbl_movie_info.setSizePolicy(size_policy)
        self.lbl_movie_info.setText(NOT_AVAILABLE)

    def setup_finishes_key_label(self):
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.lbl_finishes_key.setSizePolicy(size_policy)
        self.lbl_finishes_key.setText("Ends:")

    def setup_movie_info_key_label(self):
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.lbl_movie_info_key.setSizePolicy(size_policy)
        self.lbl_movie_info_key.setText("Info:")

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


class ListWidgetItem(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = QLabel()
        # Need to set the font explicitly as `setItemWidget` changes the font
        # to default (Segoe UI, 9pt)
        self.title.setFont(QFont("Roboto", FONT_SIZE, QFont.DemiBold))

        self.title.setAlignment(Qt.AlignVCenter)

        self.info = QLabel()
        self.info.setFont(QFont("Roboto", FONT_SIZE - 2))

        self.vlayout = QVBoxLayout()
        # self.vlayout.addStretch()
        self.vlayout.setContentsMargins(5, 0, 0, 0)
        self.vlayout.setSpacing(0)

        self.vlayout.addWidget(self.title)
        self.vlayout.setAlignment(Qt.AlignVCenter)
        # self.vlayout.addWidget(self.info)

        self.icon = QLabel()

        self.hlayout = QHBoxLayout()
        # self.hlayout.addStretch()
        self.hlayout.setContentsMargins(5, 0, 0, 0)
        self.hlayout.setSpacing(0)

        self.hlayout.addWidget(self.icon, 0)
        self.hlayout.addLayout(self.vlayout, 1)

        self.setLayout(self.hlayout)
