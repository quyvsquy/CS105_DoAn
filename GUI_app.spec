# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['GUI_app.py'],
             pathex=['/media/quocquy/DATA/1_UBUNTU_FIX_WINDOWNS/HKVI/CS105_DoHoaMayTinh/DoAnCuoiKy/CS105_DoAn'],
             binaries=[],
             datas=[],
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
          name='GUI_app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
