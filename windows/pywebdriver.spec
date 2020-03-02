# -*- mode: python ; coding: utf-8 -*-

import os
VENV = os.environ["HOME"] + "\\pywebdriver-venv"

block_cipher = None


a = Analysis(['..\\pywebdriverd'],
             # ['waitress_server.py'], # if you want waitress
             pathex=[VENV],
             binaries=[('libusb0.dll', '.'),],
             datas=[('config.ini', 'config'),
             ('capabilities.json', 'escpos'),
             # ('..\\privkey.pem', '.'),
             # ('..\\cert.pem', '.'),
             ('..\\pywebdriver\\templates\\*', 'pywebdriver\\templates'),
             ('..\\pywebdriver\\static\\css\\*', 'pywebdriver\\static\\css'),
             ('..\\pywebdriver\\static\\images\\*', 'pywebdriver\\static\\images'),
             ('..\\pywebdriver\\static\\js\\*', 'pywebdriver\\static\\js'),
             ('..\\pywebdriver\\translations\\*', 'pywebdriver\\translations'),
             ('..\\pywebdriver\\translations\\fr', 'pywebdriver\\translations\\fr'),
             (VENV + '\\Lib\\site-packages\\pif\\checkers\\dyndns', 'pif\\checkers\\dyndns'),
             (VENV + '\\Lib\\site-packages\\pif\\checkers\\httpbin', 'pif\\checkers\\httpbin'),
             (VENV + '\\Lib\\site-packages\\pif\\checkers\\icanhazip', 'pif\\checkers\\icanhazip'),
             (VENV + '\\Lib\\site-packages\\pif\\checkers\\ident', 'pif\\checkers\\ident'),
             (VENV + '\\Lib\\site-packages\\pif\\checkers\\ip42', 'pif\\checkers\\ip42'),
             (VENV + '\\Lib\\site-packages\\pif\\checkers\\ipecho', 'pif\\checkers\\ipecho'),
             (VENV + '\\Lib\\site-packages\\pif\\checkers\\ipify', 'pif\\checkers\\ipify'),
             (VENV + '\\Lib\\site-packages\\pif\\checkers\\myexternalip', 'pif\\checkers\\myexternalip'),
             (VENV + '\\Lib\\site-packages\\pif\\checkers\\tnx', 'pif\\checkers\\tnx'),
             (VENV + '\\Lib\\site-packages\\pif\\checkers\\whatismyip', 'pif\\checkers\\whatismyip'),
             (VENV + '\\Lib\\site-packages\\pif\\checkers\\wtfismyip', 'pif\\checkers\\wtfismyip'),
             ],
             hiddenimports=['pywebdriver.plugins.cups_driver', 'pywebdriver.plugins.display_driver',
             'pywebdriver.plugins.escpos_driver', 'pywebdriver.plugins.serial_driver',
             'pywebdriver.plugins.signature_driver', 'pywebdriver.plugins.telium_driver',
             'pywebdriver.plugins.opcua_driver', 'pywebdriver.plugins.odoo7', 'pywebdriver.plugins.odoo8',
             'pywebdriver.plugins.win32print_driver',
             'win32timezone', 'usb', 'requests', 'pkg_resources.py2_warn'],
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
          [],
          exclude_binaries=True,
          name='pywebdriver',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='pywebdriver')
