# -*- mode: python ; coding: utf-8 -*-
# https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable#22-customizing-the-spec-file
from pathlib import Path


def list_dir(directory, pattern="*"):
    directory = Path(directory)
    res = []
    for f in directory.rglob(pattern):
        if f.is_file():
            rel_path = f.relative_to(directory.parent)
            res.append((rel_path.as_posix(), rel_path.parent.as_posix()))
    return res


block_cipher = None


a = Analysis(
    ["folderplay/__main__.py"],
    pathex=[],
    binaries=[],
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
    name="FolderPlay",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)
