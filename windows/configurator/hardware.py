"""Deteccion de hardware en Windows: impresoras, puertos COM, dispositivos USB."""

import sys


def list_win32_printers():
    if sys.platform != "win32":
        return []
    try:
        import win32print
    except ImportError:
        return []
    try:
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS,
            None,
            2,
        )
    except Exception:
        return []
    return [
        {
            "name": item.get("pPrinterName", ""),
            "port": item.get("pPortName", ""),
            "driver": item.get("pDriverName", ""),
        }
        for item in printers
        if item.get("pPrinterName")
    ]


def list_com_ports():
    try:
        from serial.tools import list_ports
    except ImportError:
        return []
    ports = []
    for port in list_ports.comports():
        ports.append(
            {
                "device": port.device,
                "description": port.description or "",
                "hwid": port.hwid or "",
            }
        )
    return ports


def list_usb_devices():
    try:
        import usb.core
    except ImportError:
        return []
    devices = []
    try:
        for dev in usb.core.find(find_all=True):
            try:
                manufacturer = usb.util.get_string(dev, dev.iManufacturer) or ""
            except Exception:
                manufacturer = ""
            try:
                product = usb.util.get_string(dev, dev.iProduct) or ""
            except Exception:
                product = ""
            devices.append(
                {
                    "vendor_id": "0x%04x" % dev.idVendor,
                    "product_id": "0x%04x" % dev.idProduct,
                    "manufacturer": manufacturer,
                    "product": product,
                }
            )
    except Exception:
        return []
    return devices


def detect_all():
    return {
        "win32_printers": list_win32_printers(),
        "com_ports": list_com_ports(),
        "usb_devices": list_usb_devices(),
    }
