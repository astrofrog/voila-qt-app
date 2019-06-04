# -*- mode: python ; coding: utf-8 -*-

import os
import glob

block_cipher = None

notebooks = [(x, 'app_notebooks') for x in glob.glob(os.path.join('app_notebooks', '*.ipynb'))]

a = Analysis(['voila_demo.py'],
             pathex=['voila-qt'],
             binaries=[],
             datas=notebooks,
             hiddenimports=['voila',
                            'ipykernel',
                            'ipykernel.datapub',
                            'ipywidgets',
                            'jupyterlab_pygments',
                            'storemagic',
                            'ipyvuetify',
                            'bqplot'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='voila_demo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='voila_demo')

app = BUNDLE(coll,
             name='voila_demo.app',
             info_plist={
             'NSHighResolutionCapable': 'True'
             },
             bundle_identifier='org.qt-project.Qt.QtWebEngineCore')
