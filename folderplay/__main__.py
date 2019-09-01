import logging
import os
import sys

import click
from PyQt5.QtCore import Qt, QFileInfo, QCoreApplication
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication

from folderplay import __version__ as about
from folderplay.constants import FONT_SIZE
from folderplay.gui.icons import IconSet
from folderplay.gui.styles import Style
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


def validate_player(ctx, param, value):
    if not value:
        return value
    file_info = QFileInfo(value)
    if not file_info or not file_info.isExecutable():
        raise click.BadParameter("Player must an executable")
    return value


def get_style_by_name(ctx, param, value):
    if not value:
        return value
    try:
        return Style.get(value)
    except ValueError as e:
        raise click.BadParameter(e)


def get_icon_set_by_name(ctx, param, value):
    if not value:
        return value
    try:
        return IconSet.get(value)
    except ValueError as e:
        raise click.BadParameter(e)


@click.command(short_help=about.__description__)
@click.version_option(about.__version__)
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
@click.option(
    "--style",
    "-s",
    type=click.Choice(Style.names()),
    metavar="<name>",
    help="Color style: {}".format(", ".join(Style.names())),
    callback=get_style_by_name,
)
@click.option(
    "--icons",
    "-i",
    type=click.Choice(IconSet.names()),
    metavar="<name>",
    help="Icon set: {}".format(", ".join(IconSet.names())),
    callback=get_icon_set_by_name,
)
@click.argument(
    "workdir",
    metavar="<directory>",
    type=click.Path(
        exists=True, file_okay=False, readable=True, resolve_path=True
    ),
    default=os.getcwd(),
    nargs=1,
)
def main(workdir, player_path, style, icons):
    setup_logging()

    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(
        resource_path("fonts/Roboto/Roboto-Regular.ttf")
    )

    font = QFont("Roboto", FONT_SIZE)
    QApplication.setFont(font)

    player = Player(workdir, style, icons)
    player.show()

    if player_path:
        player.local_player.set_player(player_path)
        player.update_player_info()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(prog_name="fplay")
