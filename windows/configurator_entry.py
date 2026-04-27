"""Wrapper script utilizado por PyInstaller como entry point del configurador.

PyInstaller no soporta `python -m` como entry, asi que se necesita un .py top-level.
"""

from windows.configurator.main import main

if __name__ == "__main__":
    raise SystemExit(main())
