# -*- mode: python -*-

block_cipher = None


a = Analysis(['Ring.pyw'],
             pathex=['C:\\Users\\Coal\\Downloads\\Ring'],
             binaries=None,
             datas=None,
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
          name='Ring',
          debug=False,
          strip=False,
          upx=False,
          console=False , icon='icon.ico')
