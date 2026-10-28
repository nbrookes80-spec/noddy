; Inno Setup script. Build with: iscc /DAppVersion=0.1.0 packaging\windows\TunerToolPro.iss
; Expects the PyInstaller output in dist\TunerToolPro (see .github/workflows/windows.yml).
#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif

[Setup]
AppId={{6F1D7C42-5B0E-4C0A-9A53-7E2B1D9C4A10}
AppName=TunerToolPro
AppVersion={#AppVersion}
AppPublisher=TunerToolPro
DefaultDirName={autopf}\TunerToolPro
DefaultGroupName=TunerToolPro
LicenseFile=..\..\LICENSE
SetupIconFile=TunerToolPro.ico
UninstallDisplayIcon={app}\TunerToolPro.exe
OutputDir=..\..\dist-installer
OutputBaseFilename=TunerToolPro-{#AppVersion}-setup
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked

[Files]
Source: "..\..\dist\TunerToolPro\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\TunerToolPro"; Filename: "{app}\TunerToolPro.exe"
Name: "{autodesktop}\TunerToolPro"; Filename: "{app}\TunerToolPro.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\TunerToolPro.exe"; Description: "Start TunerToolPro"; Flags: nowait postinstall skipifsilent

; Settings under %APPDATA%\TunerToolPro are deliberately left alone on uninstall.
