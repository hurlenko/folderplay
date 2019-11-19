from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QLabel, QSizePolicy

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
