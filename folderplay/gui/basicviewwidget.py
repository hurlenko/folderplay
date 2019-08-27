from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QProgressBar,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
)

from folderplay.constants import NOT_AVAILABLE, FINISHED
from folderplay.gui.button import ScalablePushButton
from folderplay.gui.groupbox import ElidedGroupBox
from folderplay.gui.label import ElidedLabel
from folderplay.utils import resource_path


class BasicViewWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Play button
        self.btn_play = ScalablePushButton(self)
        self.setup_play_button()

        # Advanced view button
        self.btn_advanced = ScalablePushButton(self)
        self.setup_advanced_button()

        self.btn_refresh = ScalablePushButton(self)
        self.setup_refresh_button()

        # Progressbar
        self.pbr_watched = QProgressBar(self)
        self.setup_progress_bar()

        # Media info groupbox
        self.grp_current_media = ElidedGroupBox(self)
        self.setup_current_media_group_box()

        self.lbl_finishes_value = ElidedLabel(self)
        self.setup_finishes_label()

        self.lbl_movie_info_value = ElidedLabel(self)
        self.setup_movie_info_label()

        self.setLayout(self.get_layout())
        self.layout().setContentsMargins(0, 0, 0, 0)

    def get_layout(self):
        vlayout = QVBoxLayout()
        vlayout_refresh_advanced = QVBoxLayout()

        hlayout = QHBoxLayout()

        mediainfo_layout = QFormLayout()
        mediainfo_layout.addRow("Ends:", self.lbl_finishes_value)
        mediainfo_layout.addRow("Info:", self.lbl_movie_info_value)

        widgets = [self.btn_advanced, self.btn_refresh]
        for w in widgets:
            vlayout_refresh_advanced.addWidget(w)

        self.grp_current_media.setLayout(mediainfo_layout)

        hlayout.addWidget(self.pbr_watched)
        hlayout.addLayout(vlayout_refresh_advanced)

        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.grp_current_media)
        vlayout.addWidget(self.btn_play)
        return vlayout

    def setup_play_button(self):
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

    def setup_refresh_button(self):
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.btn_refresh.setSizePolicy(size_policy)
        self.btn_refresh.setToolTip("Refresh")
        self.btn_refresh.setIcon(
            QIcon(resource_path("assets/icons/refresh.svg"))
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

    def setup_current_media_group_box(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.grp_current_media.setSizePolicy(size_policy)
        self.grp_current_media.setTitle(FINISHED)

    def setup_finishes_label(self):
        # size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.lbl_finishes_value.setSizePolicy(size_policy)
        self.lbl_finishes_value.setText(NOT_AVAILABLE)

    def setup_movie_info_label(self):
        # size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.lbl_movie_info_value.setSizePolicy(size_policy)
        self.lbl_movie_info_value.setText(NOT_AVAILABLE)
