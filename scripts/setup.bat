@echo off
echo ====== Enabling script execution =======
powershell Set-ExecutionPolicy RemoteSigned -Scope CurrentUser 

@REM Installing scoop, the 'non' command-line installer for Windows
echo ====== Installing Scoop and stuff =======
powershell irm get.scoop.sh -outfile 'install.ps1'
powershell .\install.ps1 -RunAsAdmin
powershell scoop update
powershell scoop install neofetch
powershell scoop install curl
powershell rm %USERPROFILE%\windotfiles\install.ps1

@REM Installing Oh-my-posh
echo ====== Installing Oh-my-posh =======
powershell Set-ExecutionPolicy Bypass -Scope Process -Force; Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://ohmyposh.dev/install.ps1'))
echo ====== Remember to install FuraMono font =======
powershell oh-my-posh font install

@REM Installing PowerToys
echo ====== Installing PowerToys =======
powershell winget install Microsoft.PowerToys --source winget

@REM Installing tilling windo manager
echo ====== Installing GlazeWM (tilling window manager) =======
powershell curl -o %USERPROFILE%\windotfiles\GlazeWM\GlazeWM.exe https://github.com/lars-berger/GlazeWM/releases/download/v1.11.1/GlazeWM_x64_1.11.1.exe

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
 
 @REM Unistall batch