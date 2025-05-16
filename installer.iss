[Setup]
AppName=EVE PI GUI Calculator
AppVersion=1.0
DefaultDirName={pf}\EVE PI GUI Calculator
DefaultGroupName=EVE PI GUI Calculator
OutputBaseFilename=EVE_PI_GUI_Calculator_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "build\exe.win-amd64-3.12\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\EVE PI GUI Calculator"; Filename: "{app}\eve_pi_gui_calculator.exe"
Name: "{group}\Uninstall EVE PI GUI Calculator"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\eve_pi_gui_calculator.exe"; Description: "Launch EVE PI GUI Calculator"; Flags: nowait postinstall skipifsilent
