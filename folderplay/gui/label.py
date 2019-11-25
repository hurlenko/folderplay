import datetime
from enum import Enum, auto

from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (
    QLabel,
    QSizePolicy,
    QStylePainter,
    QStyleOptionButton,
    QStyle,
)

from folderplay.constants import NOT_AVAILABLE
from folderplay.gui.button import ScalablePushButton
from folderplay.utils import format_duration


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
        self.setStyleSheet(
            """
        QPushButton {
            border: none;
        }
        QPushButton[alignleft=true] {
          text-align: left;
        }
        """
        )


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


class MarqueeLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.px = 0
        self.py = 0
        self._speed = 1
        self._pauseDuration = 2e3
        self._separatorWidth = 10
        self.timer = QTimer(self)
        self.textLength = 0
        self.fontPointSize = 0
        self.setFixedHeight(self.fontMetrics().height())

    def setFont(self, font):
        super().setFont(font)
        self.setFixedHeight(self.fontMetrics().height())

    def setText(self, text):
        super().setText(text)
        self.initScroll()

    def updateCoordinates(self):
        self.px = 0
        self.py = self.height() / 2
        self.fontPointSize = self.font().pointSize() / 2
        self.textLength = self.fontMetrics().width(self.text())

    def resizeEvent(self, event):
        self.updateCoordinates()
        super().resizeEvent(event)

    def initScroll(self):
        self.updateCoordinates()
        self.timer.stop()
        if self.textLength > self.width():
            self.timer.timeout.connect(self.update)
            self.timer.setInterval(1000 // 60)  # 60 FPS
            self.timer.singleShot(self._pauseDuration, self.timer.start)

    def paintEvent(self, event):
        if not self.timer.isActive():
            return super().paintEvent(event)
        painter = QPainter(self)
        self.px -= self.speed()
        if self.px <= -self.textLength - self._separatorWidth:
            self.px = 0
            self.timer.stop()
            self.timer.singleShot(self._pauseDuration, self.timer.start)

        painter.drawText(self.px, self.py + self.fontPointSize, self.text())
        painter.drawText(
            self.px + self.textLength + self._separatorWidth,
            self.py + self.fontPointSize,
            self.text(),
        )
        painter.translate(self.px, 0)

    def speed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed


class DurationLabel(QIconLabel):
    class DisplayMode(Enum):
        duration = auto()
        endtime = auto()

        @classmethod
        def names(cls):
            return [e.name for e in cls]

    def __init__(
        self, duration: int, display_mode: DisplayMode, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.pressed.connect(self._toggle_mode)
        self.setCheckable(True)
        self.duration = duration
        self.display_mode = display_mode
        self.update_title()

    def set_duration(self, duration: int):
        self.duration = duration
        self.update_title()

    def set_display_mode(self, mode: DisplayMode):
        if isinstance(mode, str):
            mode = self.DisplayMode[mode]
        self.display_mode = mode
        self.update_title()

    def update_title(self):
        if not self.duration:
            text = NOT_AVAILABLE
            tooltip = NOT_AVAILABLE
        elif self.display_mode == self.DisplayMode.endtime:
            tooltip = "Ends"
            now = datetime.datetime.now()
            finishes = now + datetime.timedelta(seconds=self.duration)
            text = finishes.strftime("%H:%M")
        else:
            tooltip = "Duration"
            text = format_duration(self.duration)
        self.setText(text)
        self.setToolTip(tooltip)

    def _toggle_mode(self):
        if self.display_mode == self.DisplayMode.duration:
            self.display_mode = self.DisplayMode.endtime
        else:
            self.display_mode = self.DisplayMode.duration
        self.update_title()
