import logging
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication

from folderplay.constants import FONT_SIZE
from folderplay.player import Player


def setup_logging():
    handlers = [logging.StreamHandler(sys.stdout)]
    logging.basicConfig(
        handlers=handlers,
        format=(
            "{asctime:^} | {levelname: ^8} | "
            "{filename: ^14} {lineno: <4} | {message}"
        ),
        style="{",
        datefmt="%d.%m.%Y %H:%M:%S",
        level=logging.DEBUG,
    )


def main():
    setup_logging()

    QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    QFontDatabase.addApplicationFont("assets/fonts/Roboto/Roboto-Regular.ttf")

    font = QFont("Roboto", FONT_SIZE)
    QApplication.setFont(font)

    app.setStyle("Fusion")
    player = Player(os.getcwd())
    player.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
