"""Metadata de drivers disponibles en PyWebDriver.

Cada driver se describe con:
- key: identificador interno (coincide con [application] drivers= y nombre del modulo)
- label: nombre legible (es/en)
- description: explicacion corta (es/en)
- section: seccion en config.ini (None si no requiere config propia)
- platform: 'all', 'windows', 'linux'
- recommended: incluido por defecto en instalaciones tipicas
- fields: lista de campos de configuracion para el formulario dinamico
"""

DRIVERS = [
    {
        "key": "odoo8",
        "label": {"es": "Compatibilidad Odoo 8+", "en": "Odoo 8+ compatibility"},
        "description": {
            "es": "Activa la compatibilidad con el POS de Odoo. Imprescindible si se usa Odoo.",
            "en": "Enables Odoo POS compatibility. Required if using Odoo.",
        },
        "section": None,
        "platform": "all",
        "recommended": True,
        "fields": [],
    },
    {
        "key": "win32print_driver",
        "label": {"es": "Impresora Windows generica", "en": "Generic Windows printer"},
        "description": {
            "es": "Imprime usando el driver de Windows (cualquier impresora instalada).",
            "en": "Prints via the Windows driver (any installed printer).",
        },
        "section": None,
        "platform": "windows",
        "recommended": True,
        "fields": [],
    },
    {
        "key": "escpos_driver",
        "label": {"es": "Impresora ESC/POS", "en": "ESC/POS printer"},
        "description": {
            "es": "Impresora termica Epson/compatible (USB, serial o Win32).",
            "en": "Epson/compatible thermal printer (USB, serial or Win32).",
        },
        "section": "escpos_driver",
        "platform": "all",
        "recommended": True,
        "fields": [
            {
                "key": "device_type",
                "label": {"es": "Tipo de conexion", "en": "Connection type"},
                "type": "select",
                "options": ["win32", "usb", "serial"],
                "default": "win32",
            },
            {
                "key": "printer_names",
                "label": {"es": "Nombres de impresora (Win32, comodines OK)", "en": "Printer names (Win32, wildcards OK)"},
                "type": "text",
                "default": "EPSON TM*",
                "depends_on": {"device_type": "win32"},
                "datasource": "win32_printers",
            },
            {
                "key": "serial_device_name",
                "label": {"es": "Puerto serial", "en": "Serial port"},
                "type": "select",
                "default": "COM1",
                "depends_on": {"device_type": "serial"},
                "datasource": "com_ports",
            },
            {
                "key": "serial_baudrate",
                "label": {"es": "Baudrate", "en": "Baudrate"},
                "type": "number",
                "default": 9600,
                "depends_on": {"device_type": "serial"},
            },
            {
                "key": "serial_bytesize",
                "label": {"es": "Bytesize", "en": "Bytesize"},
                "type": "number",
                "default": 8,
                "depends_on": {"device_type": "serial"},
            },
            {
                "key": "serial_timeout",
                "label": {"es": "Timeout (s)", "en": "Timeout (s)"},
                "type": "number",
                "default": 1,
                "depends_on": {"device_type": "serial"},
            },
        ],
    },
    {
        "key": "display_driver",
        "label": {"es": "Display de cliente", "en": "Customer display"},
        "description": {
            "es": "Pantalla de cliente conectada por puerto serial (COM).",
            "en": "Customer-facing display connected via serial port (COM).",
        },
        "section": "display_driver",
        "platform": "all",
        "recommended": False,
        "fields": [
            {
                "key": "device_name",
                "label": {"es": "Puerto", "en": "Port"},
                "type": "select",
                "default": "auto",
                "datasource": "com_ports",
                "allow_auto": True,
            },
            {
                "key": "device_rate",
                "label": {"es": "Baudrate", "en": "Baudrate"},
                "type": "number",
                "default": 9600,
            },
            {
                "key": "device_timeout",
                "label": {"es": "Timeout (s)", "en": "Timeout (s)"},
                "type": "number",
                "default": 0.05,
                "step": 0.01,
            },
        ],
    },
    {
        "key": "telium_driver",
        "label": {"es": "Terminal de pago Ingenico/Telium", "en": "Ingenico/Telium payment terminal"},
        "description": {
            "es": "Terminal de pago con protocolo Telium 3 (Ingenico, Sagem).",
            "en": "Payment terminal using Telium 3 protocol (Ingenico, Sagem).",
        },
        "section": "telium_driver",
        "platform": "all",
        "recommended": False,
        "fields": [
            {
                "key": "device_name",
                "label": {"es": "Puerto", "en": "Port"},
                "type": "select",
                "default": "auto",
                "datasource": "com_ports",
                "allow_auto": True,
            },
            {
                "key": "device_rate",
                "label": {"es": "Baudrate", "en": "Baudrate"},
                "type": "number",
                "default": 9600,
            },
        ],
    },
    {
        "key": "adyen_driver",
        "label": {"es": "Terminal Adyen", "en": "Adyen terminal"},
        "description": {
            "es": "Terminal de pago Adyen (Terminal API 3.0).",
            "en": "Adyen payment terminal (Terminal API 3.0).",
        },
        "section": "adyen_driver",
        "platform": "all",
        "recommended": False,
        "fields": [
            {
                "key": "endpoint",
                "label": {"es": "Endpoint", "en": "Endpoint"},
                "type": "text",
                "default": "https://terminal-api-live.adyen.com/sync",
            },
            {
                "key": "api_key",
                "label": {"es": "API Key", "en": "API Key"},
                "type": "password",
                "default": "",
            },
        ],
    },
    {
        "key": "scale_driver",
        "label": {"es": "Bascula", "en": "Scale"},
        "description": {
            "es": "Bascula con protocolo Toledo o similar.",
            "en": "Scale using Toledo or similar protocol.",
        },
        "section": "scale_driver",
        "platform": "all",
        "recommended": False,
        "fields": [
            {
                "key": "protocol_name",
                "label": {"es": "Protocolo", "en": "Protocol"},
                "type": "select",
                "options": ["toledo"],
                "default": "toledo",
            },
            {
                "key": "unit",
                "label": {"es": "Unidad", "en": "Unit"},
                "type": "select",
                "options": ["kg", "g", "lb", "oz"],
                "default": "kg",
            },
            {
                "key": "port",
                "label": {"es": "Puerto", "en": "Port"},
                "type": "select",
                "default": "COM1",
                "datasource": "com_ports",
            },
            {
                "key": "baudrate",
                "label": {"es": "Baudrate", "en": "Baudrate"},
                "type": "number",
                "default": 9600,
            },
            {
                "key": "poll_interval",
                "label": {"es": "Intervalo (s)", "en": "Poll interval (s)"},
                "type": "number",
                "default": 0.5,
                "step": 0.1,
            },
        ],
    },
    {
        "key": "serial_driver",
        "label": {"es": "Puerto serial generico", "en": "Generic serial port"},
        "description": {
            "es": "Acceso directo a un puerto serial para integraciones a medida.",
            "en": "Direct access to a serial port for custom integrations.",
        },
        "section": "serial_driver",
        "platform": "all",
        "recommended": False,
        "fields": [
            {
                "key": "port",
                "label": {"es": "Puerto", "en": "Port"},
                "type": "select",
                "default": "COM3",
                "datasource": "com_ports",
            },
            {
                "key": "baudrate",
                "label": {"es": "Baudrate", "en": "Baudrate"},
                "type": "number",
                "default": 9600,
            },
            {
                "key": "bytesize",
                "label": {"es": "Bytesize", "en": "Bytesize"},
                "type": "number",
                "default": 8,
            },
            {
                "key": "parity",
                "label": {"es": "Paridad", "en": "Parity"},
                "type": "select",
                "options": ["N", "E", "O", "M", "S"],
                "default": "N",
            },
            {
                "key": "stopbits",
                "label": {"es": "Stop bits", "en": "Stop bits"},
                "type": "number",
                "default": 1,
            },
            {
                "key": "timeout",
                "label": {"es": "Timeout (s)", "en": "Timeout (s)"},
                "type": "number",
                "default": 5,
            },
        ],
    },
    {
        "key": "signature_driver",
        "label": {"es": "Captura de firma", "en": "Signature capture"},
        "description": {
            "es": "Almacena firmas SVG enviadas desde el frontend.",
            "en": "Stores SVG signatures sent from the frontend.",
        },
        "section": "signature_driver",
        "platform": "all",
        "recommended": False,
        "fields": [
            {
                "key": "signature_file",
                "label": {"es": "Archivo de firma", "en": "Signature file"},
                "type": "text",
                "default": "signature.svg",
            },
            {
                "key": "download_path",
                "label": {"es": "Ruta de descarga", "en": "Download path"},
                "type": "text",
                "default": "C:\\Temp",
            },
        ],
    },
]


def driver_by_key(key):
    for driver in DRIVERS:
        if driver["key"] == key:
            return driver
    return None


def windows_drivers():
    return [d for d in DRIVERS if d["platform"] in ("all", "windows")]


def recommended_keys():
    return [d["key"] for d in windows_drivers() if d["recommended"]]
