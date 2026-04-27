"""Wrapper alrededor de NSSM para gestionar el servicio Windows de PyWebDriver."""

import os
import subprocess

SERVICE_NAME = "Pywebdriver"
LOG_ROTATE_BYTES = 1_000_000


def _run(args, check=False):
    try:
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=30,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except FileNotFoundError as exc:
        return -1, "", str(exc)
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    if check and proc.returncode not in (0, 1):
        raise RuntimeError(proc.stderr or proc.stdout)
    return proc.returncode, proc.stdout, proc.stderr


def nssm_path(app_dir):
    return os.path.join(app_dir, "nssm.exe")


def exe_path(app_dir):
    return os.path.join(app_dir, "pywebdriver.exe")


def status(app_dir):
    nssm = nssm_path(app_dir)
    code, out, _ = _run([nssm, "status", SERVICE_NAME])
    if code != 0:
        return "not_installed"
    state = (out or "").strip().split("\n")[0].strip()
    return state or "unknown"


def install(app_dir, autostart=True):
    nssm = nssm_path(app_dir)
    exe = exe_path(app_dir)
    if not os.path.exists(nssm):
        raise FileNotFoundError(nssm)
    if not os.path.exists(exe):
        raise FileNotFoundError(exe)

    _run([nssm, "stop", SERVICE_NAME])
    _run([nssm, "remove", SERVICE_NAME, "confirm"])

    code, _, err = _run([nssm, "install", SERVICE_NAME, exe], check=True)
    if code != 0:
        raise RuntimeError(err)

    log_out = os.path.join(app_dir, "pywebdriver.out.log")
    log_err = os.path.join(app_dir, "pywebdriver.err.log")
    _run([nssm, "set", SERVICE_NAME, "AppStdout", log_out])
    _run([nssm, "set", SERVICE_NAME, "AppStderr", log_err])
    _run([nssm, "set", SERVICE_NAME, "AppRotateFiles", "1"])
    _run([nssm, "set", SERVICE_NAME, "AppRotateOnline", "1"])
    _run([nssm, "set", SERVICE_NAME, "AppRotateBytes", str(LOG_ROTATE_BYTES)])
    _run(
        [
            nssm,
            "set",
            SERVICE_NAME,
            "Start",
            "SERVICE_AUTO_START" if autostart else "SERVICE_DEMAND_START",
        ]
    )

    if autostart:
        start(app_dir)


def start(app_dir):
    code, _, err = _run([nssm_path(app_dir), "start", SERVICE_NAME])
    if code != 0:
        raise RuntimeError(err.strip() or "Could not start service")


def stop(app_dir):
    _run([nssm_path(app_dir), "stop", SERVICE_NAME])


def restart(app_dir):
    stop(app_dir)
    start(app_dir)


def remove(app_dir):
    nssm = nssm_path(app_dir)
    _run([nssm, "stop", SERVICE_NAME])
    _run([nssm, "remove", SERVICE_NAME, "confirm"])
