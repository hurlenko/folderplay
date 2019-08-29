import logging
import os
import sys

import click
from PyQt5.QtCore import Qt, QFileInfo, QCoreApplication
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication

from folderplay import __version__ as about
from folderplay.constants import FONT_SIZE
from folderplay.player import Player
from folderplay.utils import resource_path
import folderplay.gui.styles as styles
from folderplay.gui.qtmodern import ModernWindow

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


def validate_player(ctx, param, value):
    if not value:
        return value
    file_info = QFileInfo(value)
    if not file_info or not file_info.isExecutable():
        raise click.BadParameter("Player must an executable")
    return value


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
@click.option(
    "--player",
    "-p",
    "player_path",
    type=click.Path(
        exists=True, dir_okay=False, readable=True, resolve_path=True
    ),
    metavar="<path>",
    help="Host player binary",
    callback=validate_player,
)
def main(workdir, player_path):
    setup_logging()

    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    # QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)

    styles.dark(app)

    QFontDatabase.addApplicationFont(
        resource_path("fonts/Roboto/Roboto-Regular.ttf")
    )

    font = QFont("Roboto", FONT_SIZE)
    QApplication.setFont(font)

    # app.setStyle("Fusion")
    player = Player(workdir)

    # mw = ModernWindow(player)
    # mw.show()

    player.show()
    if player_path:
        player.local_player.set_player(player_path)
        player.update_player_info()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(prog_name="fplay")
