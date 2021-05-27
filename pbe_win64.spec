# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src/__main__.py'],
             pathex=['/home/hendrikboeck/DevEnv/karel/karel_the_robot_python3_backend'],
             binaries=[],
             datas=[
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
               ('assets/theme/ClickButtonMenu.json', 'assets/theme'), # dont touch
               ('assets/theme/Sidemenu.json', 'assets/theme'), # dont touch
               ('assets/theme/theme.json', 'assets/theme'), # dont touch
               ('assets/view/DebugWindow_default.xml', 'assets/view'),
               ('assets/view/ClickButtonMenu.xml', 'assets/view'),
               
               # Windows
               ('env/Lib/site-packages/pygame_gui/data/default_theme.json', 'pygame_gui/data'),
               ('env/Lib/site-packages/pygame_gui/data/FiraCode-Bold.ttf', 'pygame_gui/data'),
               ('env/Lib/site-packages/pygame_gui/data/FiraCode-Regular.ttf', 'pygame_gui/data'),
               ('env/Lib/site-packages/pygame_gui/data/FiraMono-BoldItalic.ttf', 'pygame_gui/data'),
               ('env/Lib/site-packages/pygame_gui/data/FiraMono-RegularItalic.ttf', 'pygame_gui/data'),
              ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='karel_pbe',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
