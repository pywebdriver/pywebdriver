; Script generated for PyWebDriver with graphical configurator (PyWebView).
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Odoo Pywebdriver"
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
ArchitecturesInstallIn64BitMode=x64compatible
ArchitecturesAllowed=x64compatible

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "launchconfig"; Description: "Open configurator after installation (requires administrator privileges)"; GroupDescription: "Post-installation:"; Languages: en
Name: "launchconfig"; Description: "Abrir el configurador al finalizar la instalacion (requiere privilegios de administrador)"; GroupDescription: "Pos-instalacion:"; Languages: spanish
Name: "launchconfig"; Description: "Ouvrir le configurateur après l'installation (nécessite des privilèges d'administrateur)"; GroupDescription: "Post-installation:"; Languages: french
Name: "silentdefaults"; Description: "Apply default configuration without wizard (mass deployments)"; GroupDescription: "Post-installation:"; Flags: unchecked; Languages: en
Name: "silentdefaults"; Description: "Aplicar configuracion por defecto sin asistente (despliegues masivos)"; GroupDescription: "Pos-instalacion:"; Flags: unchecked; Languages: spanish
Name: "silentdefaults"; Description: "Appliquer la configuration par défaut sans assistant (déploiements massifs)"; GroupDescription: "Post-installation:"; Flags: unchecked; Languages: french

[Dirs]
Name: "{app}"; Permissions: users-modify;

[Files]
; Bundle except config.ini (handled separately to preserve it during updates).
Source: "..\dist\pywebdriver\*"; DestDir: "{app}"; Excludes: "_internal\config\config.ini"; Permissions: users-modify; Flags: recursesubdirs ignoreversion overwritereadonly
; Config template only on first install: never overwrites user's config.
; Installed at {app}\config\ (outside _internal) so it survives upgrades and is easy to edit.
Source: "..\dist\pywebdriver\_internal\config\config.ini"; DestDir: "{app}\config"; Permissions: users-modify; Flags: onlyifdoesntexist uninsneveruninstall

[Icons]
Name: "{group}\Configure PyWebDriver"; Filename: "{app}\{#MyAppConfiguratorExeName}"; WorkingDir: "{app}"; Languages: en
Name: "{group}\Configurar PyWebDriver"; Filename: "{app}\{#MyAppConfiguratorExeName}"; WorkingDir: "{app}"; Languages: spanish
Name: "{group}\Configurer PyWebDriver"; Filename: "{app}\{#MyAppConfiguratorExeName}"; WorkingDir: "{app}"; Languages: french
Name: "{group}\Service status"; Filename: "{app}\{#MyAppConfiguratorExeName}"; WorkingDir: "{app}"; Languages: en
Name: "{group}\Estado del servicio"; Filename: "{app}\{#MyAppConfiguratorExeName}"; WorkingDir: "{app}"; Languages: spanish
Name: "{group}\État du service"; Filename: "{app}\{#MyAppConfiguratorExeName}"; WorkingDir: "{app}"; Languages: french
Name: "{group}\Installation folder"; Filename: "{app}"; Languages: en
Name: "{group}\Carpeta de instalacion"; Filename: "{app}"; Languages: spanish
Name: "{group}\Dossier d'installation"; Filename: "{app}"; Languages: french
Name: "{group}\Uninstall PyWebDriver"; Filename: "{uninstallexe}"; Languages: en
Name: "{group}\Desinstalar PyWebDriver"; Filename: "{uninstallexe}"; Languages: spanish
Name: "{group}\Désinstaller PyWebDriver"; Filename: "{uninstallexe}"; Languages: french

[Run]
; Silent mode: only writes defaults + installs service (mass deployments / /SILENT).
Filename: "{app}\{#MyAppConfiguratorExeName}"; Parameters: "--silent --install-service --generate-ssl"; Flags: runhidden waituntilterminated; Tasks: silentdefaults
; Interactive mode: launches the graphical wizard to configure everything.
Filename: "{app}\{#MyAppConfiguratorExeName}"; Description: "Configure PyWebDriver now"; Flags: postinstall nowait skipifsilent; Tasks: launchconfig; Languages: en
Filename: "{app}\{#MyAppConfiguratorExeName}"; Description: "Configurar PyWebDriver ahora"; Flags: postinstall nowait skipifsilent; Tasks: launchconfig; Languages: spanish
Filename: "{app}\{#MyAppConfiguratorExeName}"; Description: "Configurer PyWebDriver maintenant"; Flags: postinstall nowait skipifsilent; Tasks: launchconfig; Languages: french

[UninstallRun]
Filename: "{app}\{#MyAppConfiguratorExeName}"; Parameters: "--uninstall --remove-ssl"; Flags: runhidden waituntilterminated; RunOnceId: "UninstallService"
