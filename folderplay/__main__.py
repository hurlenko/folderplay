import logging
import os
import sys

import click
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication

from folderplay import __version__ as about
from folderplay.constants import FONT_SIZE
from folderplay.player import Player
from folderplay.utils import resource_path

click.echo(click.style(about.__doc__, fg="blue"))


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


@click.command(short_help=about.__description__)
@click.version_option(about.__version__)
@click.option(
    "--workdir",
    "-w",
    type=click.Path(
        exists=True, file_okay=False, readable=True, resolve_path=True
    ),
    default=os.getcwd(),
    metavar="<directory>",
    help="Working directory",
)
def main(workdir):
    setup_logging()

    QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    QFontDatabase.addApplicationFont(
        resource_path("assets/fonts/Roboto/Roboto-Regular.ttf")
    )

    font = QFont("Roboto", FONT_SIZE)
    QApplication.setFont(font)

    app.setStyle("Fusion")
    player = Player(workdir)
    player.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(prog_name="folderplay")
