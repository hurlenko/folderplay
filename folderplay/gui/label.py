import datetime
from enum import Enum, auto

from PyQt5.QtCore import Qt, QSize, QTimer, QEvent
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (
    QLabel,
    QSizePolicy,
    QStylePainter,
    QStyleOptionButton,
    QStyle,
)

from constants import NOT_AVAILABLE
from folderplay.gui.button import ScalablePushButton
from utils import format_duration


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
        self.py = 15
        self.pause_ms = 2e3
        self._direction = Qt.RightToLeft
        self.setWordWrap(True)
        self.timer = QTimer(self)
        self.timer.singleShot(self.pause_ms, self.animate)
        # self.timer.start(40)
        self._speed = 2
        self.textLength = 0
        self.fontPointSize = 0
        self.setAlignment(Qt.AlignVCenter)
        self.setFixedHeight(self.fontMetrics().height())

    def setFont(self, font):
        super().setFont(font)
        self.setFixedHeight(self.fontMetrics().height())

    def animation_cycle(self):
        if self._direction == Qt.RightToLeft:
            self.px -= self.speed()
            if self.px <= -self.textLength:
                self.px = self.width()
        else:
            self.px += self.speed()
            if self.px >= self.width():
                self.px = -self.textLength
        self.update()

    def animate(self):
        if self.textLength < self.width():
            return
        for _ in range(1000):
            if self._direction == Qt.RightToLeft:
                self.px -= self.speed()
                if self.px <= -self.textLength:
                    self.px = self.width()
            else:
                self.px += self.speed()
                if self.px >= self.width():
                    self.px = -self.textLength
            self.update()
        self.timer.singleShot(self.pause_ms, self.animate)

    def updateCoordinates(self):
        align = self.alignment()
        if align == Qt.AlignTop:
            self.py = 10
        elif align == Qt.AlignBottom:
            self.py = self.height() - 10
        elif align == Qt.AlignVCenter:
            self.py = self.height() / 2
        self.fontPointSize = self.font().pointSize() / 2
        self.textLength = self.fontMetrics().width(self.text())

    def setAlignment(self, alignment):
        self.updateCoordinates()
        super().setAlignment(alignment)

    def resizeEvent(self, event):
        self.updateCoordinates()
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawText(self.px, self.py + self.fontPointSize, self.text())
        painter.translate(self.px, 0)

    # def event(self, event):
    #     if event.type() == QEvent.Enter:
    #         self.unpause()
    #     elif event.type() == QEvent.Leave:
    #         self.pause()
    #     return super().event(event)

    def speed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

    def setDirection(self, direction):
        self._direction = direction
        if self._direction == Qt.RightToLeft:
            self.px = self.width() - self.textLength
        else:
            self.px = 0
        self.update()

    def pause(self):
        self.timer.stop()

    def unpause(self):
        self.timer.start()


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
