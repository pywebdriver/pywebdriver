@ECHO OFF
nssm.exe stop Pywebdriver
nssm.exe remove Pywebdriver confirm
nssm.exe install Pywebdriver "%~dp0pywebdriver.exe"
nssm.exe set Pywebdriver AppStdout "pywebdriver.out.log"
nssm.exe set Pywebdriver AppStderr "pywebdriver.err.log"
nssm.exe set Pywebdriver AppRotateFiles 1
nssm.exe set Pywebdriver AppRotateOnline 1
nssm.exe set Pywebdriver AppRotateBytes 1000000
nssm.exe start Pywebdriver
