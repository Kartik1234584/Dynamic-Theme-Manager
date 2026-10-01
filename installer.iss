#define MyAppName "Dynamic Theme Manager"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Kartik Sadhu"
#define MyAppExeName "Dynamic Theme Manager.exe"

[Setup]
; App Information
AppId={{2D43B597-DB3A-4F7F-A9F7-72D6D3A9C86F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; UI and Icon
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
; Output Settings
OutputDir=Output
OutputBaseFilename=DynamicThemeManager_Setup
Compression=lzma2/ultra64
SolidCompression=yes
; Architecture & OS
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
MinVersion=10.0.10240

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main executable and dependencies
Source: "dist\Dynamic Theme Manager\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Dynamic Theme Manager\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Exclude unneeded files if necessary (e.g. source code), but dist should only have PyInstaller output.

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Dirs]
Name: "{app}\cache"; Permissions: users-modify
Name: "{app}\wallpapers"; Permissions: users-modify
Name: "{app}\database"; Permissions: users-modify
Name: "{app}\settings"; Permissions: users-modify
