from enum import Enum, auto

from PyQt5.QtWidgets import QProgressBar


class BidirectionalProgressBar(QProgressBar):
    class Direction(Enum):
        forward = auto()
        backward = auto()

        @classmethod
        def names(cls):
            return [e.name for e in cls]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = self.Direction.forward
        self._min = 0
        self._max = 0
        self._val = 0

    def setMinimum(self, minimum: int) -> None:
        self._min = minimum
        self.update_format()

    def setMaximum(self, maximum: int) -> None:
        self._max = maximum
        self.update_format()

    def setValue(self, value: int) -> None:
        self._val = value
        self.update_format()

    def set_direction(self, direction: Direction):
        if isinstance(direction, str):
            direction = self.Direction[direction]
        self.direction = direction
        self.update_format()

    def mousePressEvent(self, event):
        self._toggle_direction()

    def update_format(self):
        format_ = "%v / %m"
        min_ = self._min
        max_ = self._max
        val_ = self._val
        if self.direction == self.Direction.backward:
            format_ = "%v"
            val_ = val_ - max_
            min_ = -max_
            max_ = 0
        super().setMinimum(min_)
        super().setMaximum(max_)
        super().setValue(val_)
        self.setFormat(format_)

    def _toggle_direction(self):
        if self.direction == self.Direction.forward:
            self.direction = self.Direction.backward
        else:
            self.direction = self.Direction.forward
        self.update_format()
