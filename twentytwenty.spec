# -*- mode: python ; coding: utf-8 -*-
import sys


a = Analysis(
    ['twentytwenty.py'],
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
    name='twentytwenty',
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
)

if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='TwentyTwenty.app',
        icon=None,
        bundle_identifier='com.paulschweigert.twentytwenty',
        info_plist={
            'CFBundleName': 'TwentyTwenty',
            'CFBundleDisplayName': 'Twenty Twenty',
            'CFBundleShortVersionString': '0.1.0',
            'NSHighResolutionCapable': True,
            'LSUIElement': True,  # hides from Dock; lives in menu bar only
        },
    )
