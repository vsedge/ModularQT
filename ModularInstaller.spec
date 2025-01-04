# ModularInstaller.spec
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os
from pathlib import Path

desktop_path = os.path.expanduser("~/Desktop")
main_script = os.path.join(desktop_path, "main.py")
icon_file = os.path.join(desktop_path, "modular.ico")

hiddenimports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.sip'
]

datas = collect_data_files('PyQt6')

a = Analysis(
    [main_script],
    pathex=[desktop_path],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ModularInstaller',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
    uac_admin=True,
)
