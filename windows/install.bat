@ECHO OFF
%~dp0nssm.exe install Pywebdriver "%~dp0pywebdriver.exe"
mkdir c:\pywebdriver 2>NUL
%~dp0nssm.exe set Pywebdriver AppStdout "C:\pywebdriver\pywebdriver.out.log"
%~dp0nssm.exe set Pywebdriver AppStderr "C:\pywebdriver\pywebdriver.err.log"
%~dp0nssm.exe set Pywebdriver AppRotateFiles 1
%~dp0nssm.exe set Pywebdriver AppRotateOnline 1
%~dp0nssm.exe set Pywebdriver AppRotateBytes 1000000
%~dp0nssm.exe restart Pywebdriver
