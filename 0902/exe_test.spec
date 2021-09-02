# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['exe_test.py'],
             pathex=['C:\\Users\\NEUROPHET\\PycharmProjects\\pythonProject\\0902'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
# Avoid warning
to_remove = ["_AES", "_ARC4", "_DES", "_DES3", "_SHA256", "_counter"]
for b in a.binaries:
    found = any(
        f'{crypto}.cp37-win_amd64.pyd' in b[1]
        for crypto in to_remove
    )
    if found:
        print(f"Removing {b[1]}")
        a.binaries.remove(b)
exe = EXE(pyz,
          a.scripts,
          [('W ignore', None, 'OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='exe_test',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
