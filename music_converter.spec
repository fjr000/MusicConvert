# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

block_cipher = None
project_root = Path.cwd()
ffmpeg_dir = project_root / "tools" / "ffmpeg"
musicdecrypto_dir = project_root / "tools" / "musicdecrypto"
datas = []

if ffmpeg_dir.exists():
    datas.append((str(ffmpeg_dir), "tools/ffmpeg"))

if musicdecrypto_dir.exists():
    datas.append((str(musicdecrypto_dir), "tools/musicdecrypto"))


a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
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
    [],
    exclude_binaries=True,
    name='音乐格式转换器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='音乐格式转换器',
)
