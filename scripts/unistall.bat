echo ====== Removing scoop =======
powershell scoop uninstall scoop
powershell rm -r %USERPROFILE%\scoop
powershell rm -r %USERPROFILE%\.config

echo ====== Removing oh-my-posh =======
powershell Uninstall-Module -Name oh-my-posh -Force

echo ====== Removing PowerToys =======
powershell winget uninstall Microsoft.PowerToys

echo ====== Removing GlazeWM (tilling window manager) =======
powershell rm %USERPROFILE%\windotfiles\GlazeWM\GlazeWM.exe

echo ====== Removing the start.bat file to the windows startup =======
powershell rm '%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start.bat'

echo ====== Removing the PowerShell profile =======
powershell rm $PROFILE

echo ====== Removing the PowerShell settings =======
set settings=(Get-Item "$Env:LocalAppData\Packages\Microsoft.WindowsTerminal_*\LocalState\settings.json")
powershell rm %settings%