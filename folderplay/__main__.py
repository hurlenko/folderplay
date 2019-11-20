import logging
import os
import shutil
import sys

import click
from PyQt5.QtCore import Qt, QFileInfo, QCoreApplication
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication

from config import Config
from folderplay import __version__ as about
from folderplay.constants import FONT_SIZE
from folderplay.gui.icons import IconSet
from folderplay.gui.styles import Style
from folderplay.player import Player
from folderplay.utils import resource_path, is_windows

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
    if file_info and file_info.isExecutable():
        return file_info.filePath()
    file_info = QFileInfo(shutil.which(value))
    if file_info and file_info.isExecutable():
        return file_info.filePath()
    if is_windows():
        from contextlib import suppress
        from pathlib import Path
        import winreg
        import itertools

        filename = Path(value.lower()).stem

        with suppress(WindowsError), winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths",
        ) as k:
            for i in itertools.count():
                subkey = winreg.EnumKey(k, i)
                if Path(subkey.lower()).stem == filename:
                    with winreg.OpenKey(k, subkey) as filekey:
                        val, _ = winreg.QueryValueEx(filekey, None)
                        file_info = QFileInfo(val)
                        if file_info and file_info.isExecutable():
                            return file_info.filePath()
    raise click.BadParameter("Player must an executable")


# def get_style_by_name(ctx, param, value):
#     if not value:
#         return value
#     try:
#         return Style.get(value)
#     except ValueError as e:
#         raise click.BadParameter(e)
#
#
# def get_icon_set_by_name(ctx, param, value):
#     if not value:
#         return value
#     try:
#         return IconSet.get(value)
#     except ValueError as e:
#         raise click.BadParameter(e)


@click.command(short_help=about.__description__)
@click.version_option(about.__version__)
@click.option(
    "--player",
    "-p",
    "player_path",
    type=click.Path(exists=False, dir_okay=False),
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
    # callback=get_style_by_name,
)
@click.option(
    "--icons",
    "-i",
    type=click.Choice(IconSet.names()),
    metavar="<name>",
    help="Icon set: {}".format(", ".join(IconSet.names())),
    # callback=get_icon_set_by_name,
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
@click.pass_context
def main(ctx, workdir, player_path, style, icons):
    setup_logging()
    config = Config(workdir, ctx.params)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(
        resource_path("fonts/Roboto/Roboto-Regular.ttf")
    )

    font = QFont("Roboto", FONT_SIZE)
    QApplication.setFont(font)

    player = Player(config)
    player.init()
    player.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main(prog_name="folderplay")
