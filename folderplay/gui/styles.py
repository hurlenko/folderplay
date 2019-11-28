from abc import ABCMeta, abstractmethod
from enum import Enum, unique

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication

from folderplay.gui.icons import IconSet
from folderplay.utils import resource_path


class AbstractStyle(metaclass=ABCMeta):
    @abstractmethod
    def apply_style(self, app):
        pass


class DarkStyle(AbstractStyle):
    _STYLESHEET = resource_path("styles/qtmodern.qss")

    def _apply_base_theme(self, app):
        """ Apply base theme to the application.

            Args:
                app (QApplication): QApplication instance.
        """

        app.setStyle("Fusion")

        with open(self._STYLESHEET) as stylesheet:
            app.setStyleSheet(stylesheet.read())

    def apply_style(self, app):
        """ Apply Dark Theme to the Qt application instance.

            Args:
                app (QApplication): QApplication instance.
        """

        darkPalette = QPalette()

        # base
        darkPalette.setColor(QPalette.WindowText, QColor(180, 180, 180))
        darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.Light, QColor(180, 180, 180))
        darkPalette.setColor(QPalette.Midlight, QColor(90, 90, 90))
        darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
        darkPalette.setColor(QPalette.Text, QColor(180, 180, 180))
        darkPalette.setColor(QPalette.BrightText, QColor(180, 180, 180))
        darkPalette.setColor(QPalette.ButtonText, QColor(180, 180, 180))
        darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
        darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
        darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.HighlightedText, QColor(180, 180, 180))
        darkPalette.setColor(QPalette.Link, QColor(56, 252, 196))
        darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        darkPalette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.ToolTipText, QColor(180, 180, 180))

        # disabled
        darkPalette.setColor(
            QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127)
        )
        darkPalette.setColor(
            QPalette.Disabled, QPalette.Text, QColor(127, 127, 127)
        )
        darkPalette.setColor(
            QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127)
        )
        darkPalette.setColor(
            QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80)
        )
        darkPalette.setColor(
            QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127)
        )

        app.setPalette(darkPalette)
        self._apply_base_theme(app)

        IconSet.current.set_color(QColor(180, 180, 180))


class LightStyle(DarkStyle):
    def apply_style(self, app):
        """ Apply Light Theme to the Qt application instance.

            Args:
                app (QApplication): QApplication instance.
        """

        lightPalette = QPalette()

        # base
        lightPalette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        lightPalette.setColor(QPalette.Button, QColor(240, 240, 240))
        lightPalette.setColor(QPalette.Light, QColor(180, 180, 180))
        lightPalette.setColor(QPalette.Midlight, QColor(200, 200, 200))
        lightPalette.setColor(QPalette.Dark, QColor(225, 225, 225))
        lightPalette.setColor(QPalette.Text, QColor(0, 0, 0))
        lightPalette.setColor(QPalette.BrightText, QColor(0, 0, 0))
        lightPalette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        lightPalette.setColor(QPalette.Base, QColor(237, 237, 237))
        lightPalette.setColor(QPalette.Window, QColor(240, 240, 240))
        lightPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
        lightPalette.setColor(QPalette.Highlight, QColor(76, 163, 224))
        lightPalette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        lightPalette.setColor(QPalette.Link, QColor(0, 162, 232))
        lightPalette.setColor(QPalette.AlternateBase, QColor(225, 225, 225))
        lightPalette.setColor(QPalette.ToolTipBase, QColor(240, 240, 240))
        lightPalette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))

        # disabled
        lightPalette.setColor(
            QPalette.Disabled, QPalette.WindowText, QColor(115, 115, 115)
        )
        lightPalette.setColor(
            QPalette.Disabled, QPalette.Text, QColor(115, 115, 115)
        )
        lightPalette.setColor(
            QPalette.Disabled, QPalette.ButtonText, QColor(115, 115, 115)
        )
        lightPalette.setColor(
            QPalette.Disabled, QPalette.Highlight, QColor(190, 190, 190)
        )
        lightPalette.setColor(
            QPalette.Disabled, QPalette.HighlightedText, QColor(115, 115, 115)
        )

        app.setPalette(lightPalette)

        self._apply_base_theme(app)
        IconSet.current.set_color(QColor(0, 0, 0))


class FusionStyle(AbstractStyle):
    def apply_style(self, app):
        app.setStyle("Fusion")
        app.setStyleSheet(
            """
        QGroupBox {
            border: 2px solid palette(midlight);
            margin-top: 30px;
        }
        """
        )
        IconSet.current.set_color(QColor(0, 0, 0))


class NativeStyle(AbstractStyle):
    def apply_style(self, app):
        app.setStyleSheet("")
        IconSet.current.set_color(QColor(0, 0, 0))


@unique
class Style(Enum):
    dark = DarkStyle()
    light = LightStyle()
    fusion = FusionStyle()
    native = NativeStyle()

    @classmethod
    def names(cls):
        return [e.name for e in cls]

    def apply(self, app):
        return self.value.apply_style(app)
