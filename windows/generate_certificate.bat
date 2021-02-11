@ECHO OFF
.\mkcert.exe -install
.\mkcert.exe localhost 127.0.0.1 ::1
mkdir c:\pywebdriver 2>NUL
copy "localhost+2.pem" c:\pywebdriver /Y
copy "localhost+2-key.pem" c:\pywebdriver /Y
