# -*- mode: python ; coding: utf-8 -*-
from sys import platform
from sys import version

if platform.startswith("win"):
  # WINDOWS
  sitepackages = "env/Lib/site-packages"
else:
  # UNIXLIKE
  print(version)
  sitepackages = "env/lib/python3.9/site-packages"

assets = [
    ('assets/64x/beeper.png', 'assets/64x'),
    ('assets/64x/karel.png', 'assets/64x'),
    ('assets/64x/tile.png', 'assets/64x'),
    ('assets/font/FiraCode-Regular.ttf', 'assets/font'),
    ('assets/font/FiraCode-Bold.ttf', 'assets/font'),
    ('assets/font/FiraCode-Light.ttf', 'assets/font'),
    ('assets/font/FiraCode-Medium.ttf', 'assets/font'),
    ('assets/font/FiraCode-Retina.ttf', 'assets/font'),
    ('assets/font/FiraCode-SemiBold.ttf', 'assets/font'),
    ('assets/font/IBMPlexMono-Regular.ttf', 'assets/font'),
    ('assets/theme/ClickButtonMenu.json', 'assets/theme'),
    ('assets/theme/GameScene.json', 'assets/theme'),
    ('assets/theme/theme.json', 'assets/theme'),
    ('assets/view/DebugWindow_default.xml', 'assets/view'),
    ('assets/view/ClickButtonMenu.xml', 'assets/view'),

    # LIB-ASSETS
    (f'{sitepackages}/pygame_gui/data/default_theme.json', 'pygame_gui/data'),
    (f'{sitepackages}/pygame_gui/data/FiraCode-Bold.ttf', 'pygame_gui/data'),
    (f'{sitepackages}/pygame_gui/data/FiraCode-Regular.ttf', 'pygame_gui/data'),
    (f'{sitepackages}/pygame_gui/data/FiraMono-BoldItalic.ttf', 'pygame_gui/data'),
    (f'{sitepackages}/pygame_gui/data/FiraMono-RegularItalic.ttf', 'pygame_gui/data')
]

print(assets)

## PYINSTALLER
#
block_cipher = None

a = Analysis(
    ['src/__main__.py'],
    pathex=['/home/hendrikboeck/DevEnv/karel/karel_the_robot_python3_backend'],
    binaries=[],
    datas=assets,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas, [],
    name='karel_pbe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False
)
