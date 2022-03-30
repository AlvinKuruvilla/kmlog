# -*- mode: python -*-
options = [ ('v', None, 'OPTION')]
block_cipher = None
a = Analysis(['src/tui.py'],
             pathex=['/Users/alvinkuruvilla/Dev/kmlog/env/lib/python3.9/site-packages' ],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='kmlog',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
