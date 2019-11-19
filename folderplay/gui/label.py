from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (
    QLabel,
    QSizePolicy,
    QStylePainter,
    QStyleOptionButton,
    QStyle,
)

from folderplay.gui.button import ScalablePushButton


class ElidedLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)

        metrics = self.fontMetrics()
        elided = metrics.elidedText(self.text(), Qt.ElideRight, self.width())

        painter.drawText(self.rect(), self.alignment(), elided)


class QIconLabel(ScalablePushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setSizePolicy(size_policy)
        self.setStyleSheet("border: none;")


class ElidedQIconLabel(QIconLabel):
    def paintEvent(self, event):
        self.setToolTip(self.text())
        painter = QStylePainter(self)
        option = QStyleOptionButton()
        self.initStyleOption(option)
        h = option.rect.height()
        w = option.rect.width()
        icon_size = max(min(h, w) - 2 * self.pad, self.minSize)
        option.iconSize = QSize(icon_size, icon_size)
        metrics = self.fontMetrics()
        elided = metrics.elidedText(
            self.text(), Qt.ElideRight, self.width() - icon_size
        )
        option.text = elided

        painter.drawControl(QStyle.CE_PushButton, option)
