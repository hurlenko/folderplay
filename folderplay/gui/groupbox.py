from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox,
    QStylePainter,
    QStyleOptionGroupBox,
    QStyle,
)


class ElidedGroupBox(QGroupBox):
    def paintEvent(self, event):
        self.setToolTip(self.title())
        painter = QStylePainter(self)
        option = QStyleOptionGroupBox()
        self.initStyleOption(option)

        metrics = self.fontMetrics()
        elided = metrics.elidedText(self.title(), Qt.ElideRight, self.width())
        option.text = elided

        painter.drawComplexControl(QStyle.CC_GroupBox, option)

# class ElidedGroupBox(QGroupBox):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.setStyleSheet("QGroupBox{padding-top:0; margin-top: 0}")
#
#     def setTitle(self, text):
#         pass
