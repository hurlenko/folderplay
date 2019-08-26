from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout

from folderplay.constants import FONT_SIZE


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
