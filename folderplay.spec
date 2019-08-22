# -*- mode: python ; coding: utf-8 -*-
# https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable#22-customizing-the-spec-file
from pathlib import Path

from pymediainfo import MediaInfo

from folderplay import __version__ as about
from folderplay import utils


def list_dir(directory, pattern="*"):
    directory = Path(directory)
    res = []
    for f in directory.rglob(pattern):
        if f.is_file():
            rel_path = f.relative_to(directory.parent)
            res.append((rel_path.as_posix(), rel_path.parent.as_posix()))
    return res


def generate_filename():
    name_parts = [about.__title__, about.__version__]
    if utils.is_linux():
        name_parts.append("linux")
    elif utils.is_windows():
        name_parts.append("windows")
    elif utils.is_macos():
        name_parts.append("darwin")

    if utils.is_os_64bit():
        name_parts.append("amd64")
    else:
        name_parts.append("386")

    return "-".join(name_parts)


def get_binaries():
    return [(MediaInfo._get_library()._name, ".")]


block_cipher = None

a = Analysis(
    ["folderplay/__main__.py"],
    pathex=[],
    binaries=[*get_binaries()],
    datas=[*list_dir("./assets")],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=generate_filename(),
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    clean=True,
    runtime_tmpdir=None,
    console=False,
    icon="assets/icons/icon.ico",
)
