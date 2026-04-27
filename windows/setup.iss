; Script generado para PyWebDriver con configurador grafico (PyWebView).
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Pywebdriver"
#define MyAppVersion "3.0.21"
#define MyAppPublisher "Akretion"
#define MyAppURL "https://github.com/pywebdriver/pywebdriver"
#define MyAppExeName "pywebdriver.exe"
#define MyAppConfiguratorExeName "pywebdriver-configurator.exe"

[Setup]
AppId={{7D8EF2D9-C39E-41B6-8DA3-698671538479}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=no
OutputBaseFilename=pywebdriver_win64_installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "launchconfig"; Description: "Abrir el configurador al finalizar la instalacion"; GroupDescription: "Pos-instalacion:"
Name: "silentdefaults"; Description: "Aplicar configuracion por defecto sin asistente (despliegues masivos)"; GroupDescription: "Pos-instalacion:"; Flags: unchecked

[Dirs]
Name: "{app}"; Permissions: users-modify;

[Files]
; Todo el bundle excepto config.ini (se trata aparte para preservarlo en updates).
Source: "..\dist\pywebdriver\*"; DestDir: "{app}"; Excludes: "config\config.ini"; Permissions: users-modify; Flags: recursesubdirs ignoreversion overwritereadonly
; Plantilla de config solo en primera instalacion: nunca pisa la del usuario.
Source: "..\dist\pywebdriver\config\config.ini"; DestDir: "{app}\config"; Permissions: users-modify; Flags: onlyifdoesntexist uninsneveruninstall

[Icons]
Name: "{group}\Configurar PyWebDriver"; Filename: "{app}\{#MyAppConfiguratorExeName}"; WorkingDir: "{app}"
Name: "{group}\Estado del servicio"; Filename: "{app}\{#MyAppConfiguratorExeName}"; WorkingDir: "{app}"
Name: "{group}\Carpeta de instalacion"; Filename: "{app}"
Name: "{group}\Desinstalar PyWebDriver"; Filename: "{uninstallexe}"

[Run]
; Modo silencioso: solo escribe defaults + instala servicio (deploys masivos / /SILENT).
Filename: "{app}\{#MyAppConfiguratorExeName}"; Parameters: "--silent --install-service --generate-ssl"; Flags: runhidden waituntilterminated; Tasks: silentdefaults
; Modo interactivo: lanza el wizard grafico para configurar todo.
Filename: "{app}\{#MyAppConfiguratorExeName}"; Description: "Configurar PyWebDriver ahora"; Flags: postinstall nowait skipifsilent; Tasks: launchconfig

[UninstallRun]
Filename: "{app}\{#MyAppConfiguratorExeName}"; Parameters: "--uninstall --remove-ssl"; Flags: runhidden waituntilterminated
