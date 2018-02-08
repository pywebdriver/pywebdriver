if "%~1"=="create" (
    echo cd %2 > "%userprofile%\desktop\ConfigurePOS.bat"
    echo notepad.exe "pkgs\pywebdriver\config\config.ini" >> "%userprofile%\desktop\ConfigurePOS.bat"
    echo nssm.exe restart pywebdriver >> "%userprofile%\desktop\ConfigurePOS.bat"
)
if "%~1"=="delete" (
    del "%userprofile%\desktop\ConfigurePOS.bat"
)
