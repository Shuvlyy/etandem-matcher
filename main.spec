# -*- mode: python ; coding: utf-8 -*-
import os
import sys

sys.path.append(os.getcwd())

from src.app_info import APP_COPYRIGHT, APP_NAME, APP_VERSION

a = Analysis(
    ["src/main.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=f"E-Tandem_Matcher_v{APP_VERSION}",
    version="file_version_info.txt",
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
    icon=["assets/logo.ico"],
)
app = BUNDLE(
    exe,
    name=f"E-Tandem_Matcher_v{APP_VERSION}.app",
    icon="assets/logo.ico",
    bundle_identifier="fr.lysandre.etandem-matcher",
    info_plist={
        "CFBundleShortVersionString": APP_VERSION,
        "CFBundleVersion": APP_VERSION,
        "NSHumanReadableCopyright": APP_COPYRIGHT,
    },
)
