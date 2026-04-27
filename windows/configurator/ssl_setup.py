"""Generacion de certificados SSL via mkcert."""

import os
import subprocess

CERT_FILE = "localhost+2.pem"
KEY_FILE = "localhost+2-key.pem"


def mkcert_path(app_dir):
    return os.path.join(app_dir, "mkcert.exe")


def generate(app_dir):
    """Genera certificados SSL en app_dir y devuelve (cert_path, key_path)."""
    mkcert = mkcert_path(app_dir)
    if not os.path.exists(mkcert):
        raise FileNotFoundError(mkcert)

    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

    install = subprocess.run(
        [mkcert, "-install"],
        cwd=app_dir,
        capture_output=True,
        text=True,
        timeout=60,
        creationflags=flags,
    )
    if install.returncode != 0:
        raise RuntimeError(install.stderr.strip() or "mkcert -install failed")

    gen = subprocess.run(
        [mkcert, "localhost", "127.0.0.1", "::1"],
        cwd=app_dir,
        capture_output=True,
        text=True,
        timeout=60,
        creationflags=flags,
    )
    if gen.returncode != 0:
        raise RuntimeError(gen.stderr.strip() or "mkcert failed")

    cert = os.path.join(app_dir, CERT_FILE)
    key = os.path.join(app_dir, KEY_FILE)
    if not os.path.exists(cert) or not os.path.exists(key):
        raise RuntimeError("Certificate files were not generated")
    return CERT_FILE, KEY_FILE


def existing(app_dir):
    cert = os.path.join(app_dir, CERT_FILE)
    key = os.path.join(app_dir, KEY_FILE)
    if os.path.exists(cert) and os.path.exists(key):
        return CERT_FILE, KEY_FILE
    return None, None


def uninstall_root_ca(app_dir):
    """Quita la CA de mkcert del trust store (idempotente)."""
    mkcert = mkcert_path(app_dir)
    if not os.path.exists(mkcert):
        return
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    subprocess.run(
        [mkcert, "-uninstall"],
        cwd=app_dir,
        capture_output=True,
        text=True,
        timeout=60,
        creationflags=flags,
    )
