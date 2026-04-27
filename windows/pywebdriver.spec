block_cipher = None

# ---- Servicio principal: pywebdriver.exe ----------------------------------

server = Analysis(
    ["..\\pywebdriverd"],
    datas=[
        ("config.ini", "config"),
        ("mkcert.exe", "."),
        ("nssm.exe", "."),
        ("capabilities.json", "escpos"),
        ("..\\pywebdriver\\templates\\*", "pywebdriver\\templates"),
        ("..\\pywebdriver\\static\\css\\*", "pywebdriver\\static\\css"),
        ("..\\pywebdriver\\static\\images\\*", "pywebdriver\\static\\images"),
        ("..\\pywebdriver\\static\\js\\*", "pywebdriver\\static\\js"),
        ("..\\pywebdriver\\translations\\*", "pywebdriver\\translations"),
        ("..\\pywebdriver\\translations\\fr", "pywebdriver\\translations\\fr"),
    ],
    hiddenimports=[
        "pywebdriver.plugins.cups_driver",
        "pywebdriver.plugins.display_driver",
        "pywebdriver.plugins.escpos_driver",
        "pywebdriver.plugins.serial_driver",
        "pywebdriver.plugins.signature_driver",
        "pywebdriver.plugins.telium_driver",
        "pywebdriver.plugins.opcua_driver",
        "pywebdriver.plugins.odoo8",
        "pywebdriver.plugins.win32print_driver",
        "pywebdriver.plugins.scale_driver",
        "pywebdriver.plugins.scale_protocols",
        "pywebdriver.plugins.scale_protocols.toledo",
        "win32timezone",
        "usb",
        "requests",
        "pkg_resources.py2_warn",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ---- Configurador GUI: pywebdriver-configurator.exe ----------------------

configurator = Analysis(
    ["configurator_entry.py"],
    pathex=[".."],
    datas=[
        ("configurator\\web\\index.html", "configurator_web"),
        ("configurator\\web\\app.js", "configurator_web"),
        ("configurator\\web\\styles.css", "configurator_web"),
        ("configurator\\web\\i18n.js", "configurator_web"),
    ],
    hiddenimports=[
        "webview",
        "webview.platforms.edgechromium",
        "webview.platforms.winforms",
        "clr_loader",
        "pythonnet",
        "win32print",
        "win32api",
        "win32con",
        "serial.tools.list_ports",
        "usb.core",
        "usb.util",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

MERGE(
    (server, "pywebdriver", "pywebdriver"),
    (configurator, "pywebdriver-configurator", "pywebdriver-configurator"),
)

server_pyz = PYZ(server.pure, server.zipped_data, cipher=block_cipher)
server_exe = EXE(
    server_pyz,
    server.scripts,
    [],
    exclude_binaries=True,
    name="pywebdriver",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

configurator_pyz = PYZ(configurator.pure, configurator.zipped_data, cipher=block_cipher)
configurator_exe = EXE(
    configurator_pyz,
    configurator.scripts,
    [],
    exclude_binaries=True,
    name="pywebdriver-configurator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    uac_admin=True,
)

coll = COLLECT(
    server_exe,
    server.binaries,
    server.zipfiles,
    server.datas,
    configurator_exe,
    configurator.binaries,
    configurator.zipfiles,
    configurator.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="pywebdriver",
)
