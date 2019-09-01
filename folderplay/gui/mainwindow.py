import logging
from pathlib import Path

from PyQt5.QtCore import QSize, Qt, QEventLoop, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow,
    QListWidget,
    QWidget,
    QVBoxLayout,
    QApplication,
    QSizePolicy,
    QAbstractItemView,
    QHBoxLayout,
)

from folderplay import __version__ as about
from folderplay.constants import MAX_MOVIE_TITLE_LENGTH, SettingsKeys
from folderplay.gui.basicviewwidget import BasicViewWidget
from folderplay.gui.icons import IconSets
from folderplay.gui.qtmodern import ModernWindow
from folderplay.gui.settingswidget import SettingsWidget
from folderplay.gui.styles import Style
from folderplay.utils import resource_path

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, media_dir: str, style: Style = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("FolderPlay by Hurlenko")
        self.setWindowIcon(QIcon(resource_path("icons/icon.ico")))
        self.media_dir = Path(media_dir)
        self.settings = QSettings(
            self.media_dir.joinpath(
                "{}.ini".format(about.__title__)
            ).as_posix(),
            QSettings.IniFormat,
        )
        self.central_widget = None
        self.set_style(style)

        self.basic_view_widget = BasicViewWidget(self)
        self.basic_view_widget.btn_advanced.clicked.connect(
            self.toggle_advanced_view
        )

        self.settings_widget = SettingsWidget(self)
        self.settings_widget.hide()

        # Media list
        self.lst_media = QListWidget(self)
        self.setup_files_list()

        # Left Pane
        self.left_pane = QWidget(self)
        self.left_pane.setLayout(self.left_pane_layout())
        self.left_pane.layout().setContentsMargins(0, 0, 0, 0)
        self.left_pane.layout().setSpacing(0)

        # Right pane
        self.right_pane = QWidget(self)
        self.right_pane.setLayout(self.right_pane_layout())
        self.right_pane.layout().setContentsMargins(0, 0, 0, 0)
        self.right_pane.layout().setSpacing(0)
        self.right_pane.hide()

        average_char_width = self.fontMetrics().averageCharWidth()
        self.left_pane_width = average_char_width * (MAX_MOVIE_TITLE_LENGTH + 5)
        self.right_pane_width = self.left_pane_width * 2

        self.left_pane.setFixedWidth(self.left_pane_width)
        self.right_pane.setFixedWidth(self.right_pane_width)
        self.central_widget.setLayout(self.advanced_view_layout())

    def set_style(self, style: Style):
        if not style:
            style_name = self.settings.value(
                SettingsKeys.STYLE, Style.light.name
            )
            style = Style.get(style_name)

        if style in (Style.dark, Style.light):
            self.central_widget = ModernWindow(self)
        else:
            self.central_widget = QWidget(self)
        style.apply(QApplication.instance())
        self.setCentralWidget(self.central_widget)
        self.settings.setValue(SettingsKeys.STYLE, style.name)

    def left_pane_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.basic_view_widget)
        layout.addWidget(self.settings_widget)
        return layout

    def right_pane_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.lst_media)
        return layout

    def advanced_view_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.left_pane)
        layout.addWidget(self.right_pane)

        return layout

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
        # self.adjustSize()
        if not self.basic_view_widget.btn_advanced.isChecked():
            self.settings_widget.hide()
            self.right_pane.hide()
        else:
            self.settings_widget.show()
            self.right_pane.show()

        self.reset()

    def reset(self):
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        self.adjustSize()
        # https://stackoverflow.com/a/30472749/8014793
        # self.setFixedSize(self.layout().sizeHint())
        # self.central_widget.adjustSize()
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

        self.central_widget.adjustSize()
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        self.setFixedSize(self.layout().sizeHint())

        # self.setFixedSize(self.central_widget.sizeHint())
        self.center()

    def setup_play_button(self):
        icon = IconSets.current().play
        self.btn_play.setIcon(icon)
        self.btn_play.setIconSize(QSize(100, 100))

    def setup_files_list(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lst_media.setSizePolicy(size_policy)
        self.lst_media.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.lst_files.setSortingEnabled(True)
        self.lst_media.setContextMenuPolicy(Qt.CustomContextMenu)
