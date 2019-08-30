from PyQt5.QtCore import Qt, QMetaObject, pyqtSlot
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolButton,
    QLabel,
    QSizePolicy,
)

from folderplay.utils import resource_path


class TitleBar(QWidget):
    """ Window dragger.

        Args:
            window (QWidget): Associated window.
            parent (QWidget, optional): Parent widget.
    """

    def __init__(self, window, parent=None):
        QWidget.__init__(self, parent)

        self._window = window
        self._mousePressed = False

        self.setObjectName("titleBar")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.lblTitle = QLabel("Title")
        self.lblTitle.setObjectName("lblTitle")
        self.lblTitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lblTitle)

        spButtons = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btnMinimize = QToolButton(self)
        self.btnMinimize.setObjectName("btnMinimize")
        self.btnMinimize.setSizePolicy(spButtons)
        layout.addWidget(self.btnMinimize)

        self.btnRestore = QToolButton(self)
        self.btnRestore.setObjectName("btnRestore")
        self.btnRestore.setSizePolicy(spButtons)
        self.btnRestore.setVisible(False)
        layout.addWidget(self.btnRestore)

        self.btnMaximize = QToolButton(self)
        self.btnMaximize.setObjectName("btnMaximize")
        self.btnMaximize.setSizePolicy(spButtons)
        layout.addWidget(self.btnMaximize)
        self.btnMaximize.setVisible(False)

        self.btnClose = QToolButton(self)
        self.btnClose.setObjectName("btnClose")
        self.btnClose.setSizePolicy(spButtons)
        layout.addWidget(self.btnClose)

    def mousePressEvent(self, event):
        self._mousePressed = True
        self._mousePos = event.globalPos()
        self._windowPos = self._window.pos()

    def mouseMoveEvent(self, event):
        if self._mousePressed:
            self._window.move(
                self._windowPos + (event.globalPos() - self._mousePos)
            )

    def mouseReleaseEvent(self, event):
        self._mousePressed = False


class ModernWindow(QWidget):
    """ Modern window.

        Args:
            w (QWidget): Main widget.
            parent (QWidget, optional): Parent widget.
    """

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        # Main frame with round borders
        self.windowFrame = QWidget(self)
        self.windowFrame.setObjectName("windowFrame")

        # Title bar and content widgets
        self.titleBar = TitleBar(self.parent(), self.windowFrame)
        self.titleBar.lblTitle.setText(self.parent().windowTitle())

        self.windowContent = QWidget(self.windowFrame)

        # windowFrame's layout that holds the titlebar and content widgets
        self.vboxFrame = QVBoxLayout(self.windowFrame)
        self.vboxFrame.setContentsMargins(0, 0, 0, 0)
        self.vboxFrame.addWidget(self.titleBar)
        self.vboxFrame.addWidget(self.windowContent)

        # Layout that holds the main frame
        self.vboxWindow = QVBoxLayout(self)
        self.vboxWindow.setContentsMargins(0, 0, 0, 0)
        self.vboxWindow.addWidget(self.windowFrame)
        # self.vboxWindow.setSizeConstraint(QLayout.SetFixedSize)

        # Disable parent's window frame
        self.parent().setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint
        )
        # Without this the edges will be sharp
        self.parent().setAttribute(Qt.WA_TranslucentBackground)

        # set stylesheet
        with open(resource_path("styles/frameless.qss")) as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # automatically connect slots
        QMetaObject.connectSlotsByName(self)

        # contentLayout = QHBoxLayout()
        # contentLayout.setContentsMargins(0, 0, 0, 0)
        # contentLayout.addWidget(w)

        # self.windowContent.setLayout(contentLayout)

        # self.setWindowTitle(parent.windowTitle())
        # self.setGeometry(parent.geometry())

        # self.installEventFilter(self)

        # Adding attribute to clean up the parent window
        # when the child is closed
        # self._w.setAttribute(Qt.WA_DeleteOnClose, True)
        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self._w.destroyed.connect(self.__child_was_closed)

    # def __child_was_closed(self):
    #     # The child was deleted, remove the reference to it and
    #     # close the parent window
    #     self._w = None
    #     self.close()

    # def eventFilter(self, source, event):
    #     if event.type() == QEvent.Close:
    #         if not self._w:
    #             return True
    #         return self._w.close()
    #
    #     return QWidget.eventFilter(self, source, event)

    @pyqtSlot()
    def on_btnMinimize_clicked(self):
        self.parent().setWindowState(Qt.WindowMinimized)

    @pyqtSlot()
    def on_btnRestore_clicked(self):
        self.titleBar.btnRestore.setVisible(False)
        # self.btnMaximize.setVisible(True)

        self.setWindowState(Qt.WindowNoState)

    @pyqtSlot()
    def on_btnMaximize_clicked(self):
        self.titleBar.btnRestore.setVisible(True)
        # self.btnMaximize.setVisible(False)

        self.setWindowState(Qt.WindowMaximized)

    @pyqtSlot()
    def on_btnClose_clicked(self):
        self.parent().close()

    # @pyqtSlot()
    # def on_titleBar_doubleClicked(self):
    #     if self.btnMaximize.isVisible():
    #         self.on_btnMaximize_clicked()
    #     else:
    #         self.on_btnRestore_clicked()
