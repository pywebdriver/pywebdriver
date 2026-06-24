"""Metadata for available drivers in PyWebDriver.

Each driver is described with:
- key: internal identifier (matches [application] drivers= and module name)
- label: readable name (English string, translated via JSON)
- description: short explanation (English string, translated via JSON)
- section: section in config.ini (None if no custom config needed)
- platform: 'all', 'windows', 'linux'
- recommended: included by default in typical installations
- fields: list of configuration fields for the dynamic form
"""

DRIVERS = [
    {
        "key": "odoo8",
        "label": "Odoo 8+ compatibility",
        "description": "Enables Odoo POS compatibility. Required if using Odoo.",
        "section": None,
        "platform": "all",
        "recommended": True,
        "fields": [],
    },
    {
        "key": "win32print_driver",
        "label": "Generic Windows printer",
        "description": "Prints via the Windows driver (any installed printer).",
        "section": None,
        "platform": "windows",
        "recommended": True,
        "fields": [],
    },
    {
        "key": "escpos_driver",
        "label": "ESC/POS printer",
        "description": "Epson/compatible thermal printer (USB, serial or Win32).",
        "section": "escpos_driver",
        "platform": "all",
        "recommended": True,
        "fields": [
            {
                "key": "device_type",
                "label": "Connection type",
                "type": "select",
                "options": ["win32", "usb", "serial"],
                "default": "win32",
            },
            {
                "key": "printer_names",
                "label": "Printer names (Win32, wildcards OK)",
                "type": "text",
                "default": "EPSON TM*",
                "depends_on": {"device_type": "win32"},
                "datasource": "win32_printers",
            },
            {
                "key": "serial_device_name",
                "label": "Serial port",
                "type": "select",
                "default": "COM1",
                "depends_on": {"device_type": "serial"},
                "datasource": "com_ports",
            },
            {
                "key": "serial_baudrate",
                "label": "Baudrate",
                "type": "number",
                "default": 9600,
                "depends_on": {"device_type": "serial"},
            },
            {
                "key": "serial_bytesize",
                "label": "Bytesize",
                "type": "number",
                "default": 8,
                "depends_on": {"device_type": "serial"},
            },
            {
                "key": "serial_timeout",
                "label": "Timeout (s)",
                "type": "number",
                "default": 1,
                "depends_on": {"device_type": "serial"},
            },
        ],
    },
    {
        "key": "display_driver",
        "label": "Customer display",
        "description": "Customer-facing display connected via serial port (COM).",
        "section": "display_driver",
        "platform": "all",
        "recommended": False,
        "fields": [
            {
                "key": "device_name",
                "label": "Port",
                "type": "select",
                "default": "auto",
                "datasource": "com_ports",
                "allow_auto": True,
            },
            {
                "key": "device_rate",
                "label": "Baudrate",
                "type": "number",
                "default": 9600,
            },
            {
                "key": "device_timeout",
                "label": "Timeout (s)",
                "type": "number",
                "default": 0.05,
                "step": 0.01,
            },
        ],
    },
    {
        "key": "telium_driver",
        "label": "Ingenico/Telium payment terminal",
        "description": "Payment terminal using Telium 3 protocol (Ingenico, Sagem).",
        "section": "telium_driver",
        "platform": "all",
        "recommended": False,
        "fields": [
            {
                "key": "device_name",
                "label": "Port",
                "type": "select",
                "default": "auto",
                "datasource": "com_ports",
                "allow_auto": True,
            },
            {
                "key": "device_rate",
                "label": "Baudrate",
                "type": "number",
                "default": 9600,
            },
        ],
    },
    {
        "key": "adyen_driver",
        "label": "Adyen terminal",
        "description": "Adyen payment terminal (Terminal API 3.0).",
        "section": "adyen_driver",
        "platform": "all",
        "recommended": False,
        "fields": [
            {
                "key": "endpoint",
                "label": "Endpoint",
                "type": "text",
                "default": "https://terminal-api-live.adyen.com/sync",
            },
            {
                "key": "api_key",
                "label": "API Key",
                "type": "password",
                "default": "",
            },
        ],
    },
    {
        "key": "scale_driver",
        "label": "Scale",
        "description": "Scale using Toledo or similar protocol.",
        "section": "scale_driver",
        "platform": "all",
        "recommended": False,
        "fields": [
            {
                "key": "protocol_name",
                "label": "Protocol",
                "type": "select",
                "options": ["toledo"],
                "default": "toledo",
            },
            {
                "key": "unit",
                "label": "Unit",
                "type": "select",
                "options": ["kg", "g", "lb", "oz"],
                "default": "kg",
            },
            {
                "key": "port",
                "label": "Port",
                "type": "select",
                "default": "COM1",
                "datasource": "com_ports",
            },
            {
                "key": "baudrate",
                "label": "Baudrate",
                "type": "number",
                "default": 9600,
            },
            {
                "key": "poll_interval",
                "label": "Poll interval (s)",
                "type": "number",
                "default": 0.5,
                "step": 0.1,
            },
        ],
    },
    {
        "key": "serial_driver",
        "label": "Generic serial port",
        "description": "Direct access to a serial port for custom integrations.",
        "section": "serial_driver",
        "platform": "all",
        "recommended": False,
        "fields": [
            {
                "key": "port",
                "label": "Port",
                "type": "select",
                "default": "COM3",
                "datasource": "com_ports",
            },
            {
                "key": "baudrate",
                "label": "Baudrate",
                "type": "number",
                "default": 9600,
            },
            {
                "key": "bytesize",
                "label": "Bytesize",
                "type": "number",
                "default": 8,
            },
            {
                "key": "parity",
                "label": "Parity",
                "type": "select",
                "options": ["N", "E", "O", "M", "S"],
                "default": "N",
            },
            {
                "key": "stopbits",
                "label": "Stop bits",
                "type": "number",
                "default": 1,
            },
            {
                "key": "timeout",
                "label": "Timeout (s)",
                "type": "number",
                "default": 5,
            },
        ],
    },
    {
        "key": "signature_driver",
        "label": "Signature capture",
        "description": "Stores SVG signatures sent from the frontend.",
        "section": "signature_driver",
        "platform": "all",
        "recommended": False,
        "fields": [
            {
                "key": "signature_file",
                "label": "Signature file",
                "type": "text",
                "default": "signature.svg",
            },
            {
                "key": "download_path",
                "label": "Download path",
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
