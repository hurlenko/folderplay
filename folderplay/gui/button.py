from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QStyleOptionButton, QStyle


class ScalablePushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pad = 1  # padding between the icon and the button frame
        self.minSize = 8  # minimum size of the icon

        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)
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
        icon_size = max(min(h, w) - 2 * self.pad, self.minSize)
        opt.iconSize = QSize(icon_size, icon_size)
        # draw button
        self.style().drawControl(QStyle.CE_PushButton, opt, qp, self)
        qp.end()
