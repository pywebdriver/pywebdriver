if "%~1"=="create" (
    if not exist %2\config.ini (
        copy %2\pkgs\pywebdriver\config\config.ini %2\config.ini
    )
    echo cd %2 > "%userprofile%\desktop\ConfigurePOS.bat"
    echo notepad.exe "config.ini" >> "%userprofile%\desktop\ConfigurePOS.bat"
    echo nssm.exe restart pywebdriver >> "%userprofile%\desktop\ConfigurePOS.bat"
)
if "%~1"=="delete" (
    del "%userprofile%\desktop\ConfigurePOS.bat"
)
