from PyQt5.QtCore import Qt, QMetaObject, pyqtSlot, QEvent
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolButton,
    QLabel,
    QSizePolicy,
)

from folderplay.utils import resource_path


class WindowDragger(QWidget):
    """ Window dragger.

        Args:
            window (QWidget): Associated window.
            parent (QWidget, optional): Parent widget.
    """

    # doubleClicked = pyqtSignal()

    def __init__(self, window, parent=None):
        QWidget.__init__(self, parent)

        self._window = window
        self._mousePressed = False

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

    #
    # def mouseDoubleClickEvent(self, event):
    #     self.doubleClicked.emit()


class ModernWindow(QWidget):
    """ Modern window.

        Args:
            w (QWidget): Main widget.
            parent (QWidget, optional): Parent widget.
    """

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self._w = parent
        self.setupUi()

        contentLayout = QHBoxLayout()
        # contentLayout.setContentsMargins(0, 0, 0, 0)
        # contentLayout.addWidget(w)

        self.windowContent.setLayout(contentLayout)

        # self.setWindowTitle(parent.windowTitle())
        # self.setGeometry(parent.geometry())

        self.installEventFilter(self)

        # Adding attribute to clean up the parent window
        # when the child is closed
        self._w.setAttribute(Qt.WA_DeleteOnClose, True)
        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self._w.destroyed.connect(self.__child_was_closed)

    def setupUi(self):
        # create title bar, content
        self.vboxWindow = QVBoxLayout(self)
        self.vboxWindow.setContentsMargins(0, 0, 0, 0)

        self.windowFrame = QWidget(self)
        self.windowFrame.setObjectName("windowFrame")
        self.windowFrame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.vboxFrame = QVBoxLayout(self.windowFrame)
        self.vboxFrame.setContentsMargins(0, 0, 0, 0)

        self.titleBar = WindowDragger(self._w, self.windowFrame)
        self.titleBar.setObjectName("titleBar")
        self.titleBar.setSizePolicy(
            QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        )

        self.hboxTitle = QHBoxLayout(self.titleBar)
        self.hboxTitle.setContentsMargins(0, 0, 0, 0)
        self.hboxTitle.setSpacing(0)

        self.lblTitle = QLabel("Title")
        self.lblTitle.setObjectName("lblTitle")
        self.lblTitle.setAlignment(Qt.AlignCenter)
        self.hboxTitle.addWidget(self.lblTitle)

        spButtons = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btnMinimize = QToolButton(self.titleBar)
        self.btnMinimize.setObjectName("btnMinimize")
        self.btnMinimize.setSizePolicy(spButtons)
        self.hboxTitle.addWidget(self.btnMinimize)

        self.btnRestore = QToolButton(self.titleBar)
        self.btnRestore.setObjectName("btnRestore")
        self.btnRestore.setSizePolicy(spButtons)
        self.btnRestore.setVisible(False)
        self.hboxTitle.addWidget(self.btnRestore)

        self.btnMaximize = QToolButton(self.titleBar)
        self.btnMaximize.setObjectName("btnMaximize")
        self.btnMaximize.setSizePolicy(spButtons)
        self.hboxTitle.addWidget(self.btnMaximize)
        self.btnMaximize.setVisible(False)

        self.btnClose = QToolButton(self.titleBar)
        self.btnClose.setObjectName("btnClose")
        self.btnClose.setSizePolicy(spButtons)
        self.hboxTitle.addWidget(self.btnClose)

        self.vboxFrame.addWidget(self.titleBar)

        self.windowContent = QWidget(self.windowFrame)
        self.windowContent.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vboxFrame.addWidget(self.windowContent)

        self.vboxWindow.addWidget(self.windowFrame)

        # set window flags
        self._w.setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._w.setAttribute(Qt.WA_TranslucentBackground)

        # set stylesheet
        with open(resource_path("styles/frameless.qss")) as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # automatically connect slots
        QMetaObject.connectSlotsByName(self)

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

    def setWindowTitle(self, title):
        """ Set window title.

            Args:
                title (str): Title.
        """

        super(ModernWindow, self).setWindowTitle(title)
        self.lblTitle.setText(title)

    @pyqtSlot()
    def on_btnMinimize_clicked(self):
        self._w.setWindowState(Qt.WindowMinimized)

    @pyqtSlot()
    def on_btnRestore_clicked(self):
        self.btnRestore.setVisible(False)
        # self.btnMaximize.setVisible(True)

        self.setWindowState(Qt.WindowNoState)

    @pyqtSlot()
    def on_btnMaximize_clicked(self):
        self.btnRestore.setVisible(True)
        # self.btnMaximize.setVisible(False)

        self.setWindowState(Qt.WindowMaximized)

    @pyqtSlot()
    def on_btnClose_clicked(self):
        self._w.close()

    # @pyqtSlot()
    # def on_titleBar_doubleClicked(self):
    #     if self.btnMaximize.isVisible():
    #         self.on_btnMaximize_clicked()
    #     else:
    #         self.on_btnRestore_clicked()
