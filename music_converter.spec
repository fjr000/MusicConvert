# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

block_cipher = None
project_root = Path.cwd()
ffmpeg_dir = project_root / "tools" / "ffmpeg"
musicdecrypto_dir = project_root / "tools" / "musicdecrypto"
inputs_dir = project_root / "inputs"
outputs_dir = project_root / "outputs"
datas = []

if ffmpeg_dir.exists():
    datas.append((str(ffmpeg_dir), "tools/ffmpeg"))

if musicdecrypto_dir.exists():
    datas.append((str(musicdecrypto_dir), "tools/musicdecrypto"))

if inputs_dir.exists():
    datas.append((str(inputs_dir), "inputs"))

if outputs_dir.exists():
    datas.append((str(outputs_dir), "outputs"))


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

# 去重：移除 PyInstaller 自动收集的 FFmpeg DLL（已通过 datas 打包到 tools/ffmpeg/）
ffmpeg_dll_names = {'avcodec-62.dll', 'avdevice-62.dll', 'avfilter-11.dll',
                    'avformat-62.dll', 'avutil-60.dll', 'swresample-6.dll', 'swscale-9.dll'}
a.binaries = [b for b in a.binaries if b[0] not in ffmpeg_dll_names]
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

# Post-build: copy inputs/outputs to root
import shutil
dist_root = Path('dist/音乐格式转换器')
internal = dist_root / '_internal'
for folder in ['inputs', 'outputs']:
    src = internal / folder
    dst = dist_root / folder
    if src.exists():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
