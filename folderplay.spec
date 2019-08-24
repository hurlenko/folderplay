# -*- mode: python ; coding: utf-8 -*-
# https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable#22-customizing-the-spec-file
import sys
from pathlib import Path

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

    if sys.maxsize > 2 ** 32:
        name_parts.append("x64")
    else:
        name_parts.append("x86")

    return "-".join(name_parts)


def get_binaries():
    # On linux libname is just a filename of the shared library located
    # somewhere on the filesystem so we need to find this file ourselves
    # (Not sure if this is the best approach)
    libs = []
    if utils.is_linux():  # Path(libname).is_absolute()
        return []
        # import subprocess
        #
        # process = subprocess.run(
        #     ["ldconfig", "-p"], capture_output=True, check=True, text=True
        # )
        # for line in process.stdout.splitlines():
        #     if libname in line:
        #         path = Path(line.split(">")[-1].strip()).resolve()
        #         libs.append((path.as_posix(), libname))
        #         break
        # else:
        #     raise RuntimeError(f"{libname} was not found")
    else:
        from pymediainfo import MediaInfo

        libname = MediaInfo._get_library()._name
        libs.append((libname, "."))

    print(libs)
    return libs


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
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    clean=True,
    runtime_tmpdir=None,
    console=False,
    icon="assets/icons/icon.ico",
)
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=False,
#     upx_exclude=[],
#     name="__main__",
# )
