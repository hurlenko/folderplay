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
)

from folderplay.constants import FONT_SIZE
from folderplay.utils import resource_path


class ScalablePushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pad = 1  # padding between the icon and the button frame
        self.minSize = 8  # minimum size of the icon

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
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
        iconSize = max(min(h, w) - 2 * self.pad, self.minSize)
        opt.iconSize = QSize(iconSize, iconSize)
        # draw button
        self.style().drawControl(QStyle.CE_PushButton, opt, qp, self)
        qp.end()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Play button
        self.btnPlay = ScalablePushButton()
        self.setup_play_button()

        # Advanced view button
        self.btnAdvanced = ScalablePushButton()
        self.setup_advanced_button()

        self.btnRefresh = ScalablePushButton()
        self.setup_refresh_button()

        # Progressbar
        self.progressBar = QProgressBar()
        self.setup_progress_bar()

        # File names list view
        self.lstFiles = QListWidget()
        self.setup_files_list()

        # Search box
        self.searchBox = QLineEdit()
        self.setup_search_line_edit()

        self.chkHideWatched = QCheckBox()
        self.setup_hide_watched_checkbox()

        self.chkRegex = QCheckBox()
        self.setup_regex_checkbox()

        self.filter_group_box = QGroupBox()
        self.setup_filter_group_box()

        self.local_player_group_box = QGroupBox()
        self.setup_local_player_group_box()

        self.player_label = QLabel()
        self.setup_player_label()

        self.player_name_label = QLabel()
        self.setup_player_name_label()

        self.advanced_view_size = QSize(1600, 600)
        self.basic_view_size = QSize(600, 250)

        self.basic_view_widgets = [
            self.btnPlay,
            self.btnAdvanced,
            self.btnRefresh,
            self.progressBar,
        ]

        self.advanced_view_widgets = [
            self.lstFiles,
            self.searchBox,
            self.chkHideWatched,
            self.chkHideWatched,
            self.chkRegex,
            self.filter_group_box,
            self.local_player_group_box,
            self.player_label,
            self.player_name_label,
        ]

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main window
        self.setup_main_window()

    def basic_view_layout(self):
        vlayout = QVBoxLayout()
        vlayout_refresh_advanced = QVBoxLayout()

        hlayout = QHBoxLayout()

        widgets = [self.btnAdvanced, self.btnRefresh]

        for w in widgets:
            vlayout_refresh_advanced.addWidget(w)

        hlayout.addWidget(self.progressBar, 3)
        hlayout.addLayout(vlayout_refresh_advanced)

        # Button is two times bigger than progressbar
        vlayout.addLayout(hlayout, 1)
        vlayout.addWidget(self.btnPlay, 2)
        return vlayout

    def advanced_view_layout(self):
        vlayout_left_pane = QVBoxLayout()
        vlayout_group_box = QVBoxLayout()
        hlayout = QHBoxLayout()

        basic_layout = self.basic_view_layout()

        hlayout_checkboxes = QHBoxLayout()
        checkboxes = [self.chkHideWatched, self.chkRegex]
        for w in checkboxes:
            hlayout_checkboxes.addWidget(w)

        hlayout_player_labels = QHBoxLayout()
        player_labels = [self.player_label, self.player_name_label]
        for w in player_labels:
            hlayout_player_labels.addWidget(w)

        self.local_player_group_box.setLayout(hlayout_player_labels)

        vlayout_group_box.addLayout(hlayout_checkboxes)
        vlayout_group_box.addWidget(self.searchBox)

        self.filter_group_box.setLayout(vlayout_group_box)

        vlayout_left_pane.addLayout(basic_layout)
        vlayout_left_pane.addWidget(self.local_player_group_box)
        vlayout_left_pane.addWidget(self.filter_group_box)

        hlayout.addLayout(vlayout_left_pane, 1)
        hlayout.addWidget(self.lstFiles, 2)

        return hlayout

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos()
        )
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def toggle_advanced_view(self):
        if self.size() == self.basic_view_size:
            for w in self.advanced_view_widgets:
                w.show()
            self.setFixedSize(self.advanced_view_size)
        else:
            for w in self.advanced_view_widgets:
                w.hide()
            self.setFixedSize(self.basic_view_size)
        self.center()

    # region Widget setup routine
    def setup_main_window(self):
        self.central_widget.setLayout(self.advanced_view_layout())
        self.setFixedSize(self.advanced_view_size)
        self.toggle_advanced_view()
        self.center()

        self.setWindowTitle("FolderPlay by Hurlenko")

    def setup_play_button(self):
        # sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # self.btnPlay.setSizePolicy(sizePolicy)
        # self.btnPlay.setText("Play")
        icon = QIcon(resource_path("assets/icons/play.svg"))
        self.btnPlay.setIcon(icon)

    def setup_advanced_button(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.btnAdvanced.setSizePolicy(sizePolicy)
        self.btnAdvanced.setToolTip("Advanced options")
        self.btnAdvanced.setCheckable(True)
        # Icons
        # https://joekuan.files.wordpress.com/2015/09/screen3.png
        self.btnAdvanced.setIcon(
            QIcon(resource_path("assets/icons/settings.svg"))
        )
        # self.btnAdvanced.setIconSize(QSize(24, 24))
        self.btnAdvanced.clicked.connect(self.toggle_advanced_view)

    def setup_refresh_button(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.btnRefresh.setSizePolicy(sizePolicy)
        self.btnRefresh.setToolTip("Refresh")
        # Icons
        # https://joekuan.files.wordpress.com/2015/09/screen3.png
        self.btnRefresh.setIcon(
            QIcon(resource_path("assets/icons/refresh.svg"))
        )
        # self.btnRefresh.setIconSize(QSize(24, 24))

    def setup_progress_bar(self):
        self.progressBar.setValue(24)
        # Allow progressbar to expand to take up all space in layout
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.progressBar.setSizePolicy(sizePolicy)

        self.progressBar.setFormat("%v / %m")
        font = self.progressBar.font()
        font.setPointSize(25)
        font.setBold(True)
        self.progressBar.setFont(font)

    def setup_files_list(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lstFiles.setSizePolicy(sizePolicy)
        self.lstFiles.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.lstFiles.setSortingEnabled(True)
        self.lstFiles.setContextMenuPolicy(Qt.CustomContextMenu)

    def setup_search_line_edit(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.searchBox.setSizePolicy(sizePolicy)
        self.searchBox.setPlaceholderText("Search...")

    def setup_regex_checkbox(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chkRegex.setSizePolicy(sizePolicy)
        self.chkRegex.setText("Regex")

    def setup_hide_watched_checkbox(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chkHideWatched.setSizePolicy(sizePolicy)
        self.chkHideWatched.setText("Hide watched")

    def setup_filter_group_box(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.filter_group_box.setSizePolicy(sizePolicy)
        self.filter_group_box.setTitle("Filter")

    def setup_local_player_group_box(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.local_player_group_box.setSizePolicy(sizePolicy)
        self.local_player_group_box.setTitle("Player")

    def setup_player_label(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.player_label.setSizePolicy(sizePolicy)
        self.player_label.setText("Name:")

    def setup_player_name_label(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.player_name_label.setSizePolicy(sizePolicy)

    # endregion Widget setup routine


class ListWidgetItem(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = QLabel()
        # Need to set the font explicitly as `setItemWidget` changes the font
        # to default (Segoe UI, 9pt)
        self.title.setFont(QFont("Roboto", FONT_SIZE, QFont.DemiBold))

        self.duration = QLabel()
        self.duration.setFont(QFont("Roboto", FONT_SIZE - 2, italic=True))

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()
        self.vlayout.setContentsMargins(5, 0, 0, 0)
        self.vlayout.setSpacing(0)

        self.vlayout.addWidget(self.title)
        self.vlayout.addWidget(self.duration)

        self.icon = QLabel()

        self.hlayout = QHBoxLayout()
        self.hlayout.addStretch()
        self.hlayout.setContentsMargins(5, 0, 0, 0)
        self.hlayout.setSpacing(0)

        self.hlayout.addWidget(self.icon, 0)
        self.hlayout.addLayout(self.vlayout, 1)

        self.setLayout(self.hlayout)
        # setStyleSheet
        # self.title.setStyleSheet(
        #     """
        #     color: rgb(0, 0, 255);
        # """
        # )
        # self.duration.setStyleSheet(
        #     """
        #     color: rgb(255, 0, 0);
        # """
        # )
