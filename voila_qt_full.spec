# -*- mode: python -*-

block_cipher = None


a = Analysis(['voila_qt_full.py'],
             pathex=['/Users/tom/Code/Hacking/voila-qt'],
             binaries=[],
             datas=[],
             hiddenimports=['PyQtWebEngine'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tkinter'],
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
          name='voila_qt_full',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='voila_qt_full.app',
             icon=None,
             bundle_identifier=None)
