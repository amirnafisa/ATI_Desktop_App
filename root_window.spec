# -*- mode: python -*-

block_cipher = None


a = Analysis(['root_window.py'],
             pathex=['/Users/Nafisa/Workspace/git-hub/ATI_Desktop_App'],
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
          name='ATI Interface',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='ATI-logo.ico')
app = BUNDLE(exe,
             name='ATI Interface.app',
             icon='ATI-logo.icns',
             bundle_identifier=None,
             info_plist={
              'NSHighResolutionCapable': 'True'
            },)
