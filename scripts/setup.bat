@REM Pasting the start bat to the shell:startup
echo ====== Copying the start.bat file to the windows startup =======
powershell cp %USERPROFILE%\windotfiles\scripts\start.bat '%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\'

@REM Creating the powershell profile
echo ====== Replacing the PowerShell profile =======
powershell cp %USERPROFILE%\windotfiles\PowerShell\Microsoft.PowerShell_profile.ps1 $PROFILE

@REM Creating the powershell profile
echo ====== Replacing the PowerShell settings =======
set settings=(Get-Item "$Env:LocalAppData\Packages\Microsoft.WindowsTerminal_*\LocalState\settings.json")
powershell cp %USERPROFILE%\windotfiles\PowerShell\settings.json %settings%

powershell %USERPROFILE%\windotfiles\scripts\start.bat

@REM https://github.com/CrypticButter/ButteryTaskbar/releases/download/v1.2.2/Buttery-Taskbar-setup.exe