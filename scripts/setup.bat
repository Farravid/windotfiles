@REM Installing scoop, the 'non' command-line installer for Windows
echo ====== Installing Scoop and stuff =======
powershell iex (new-object net.webclient).downloadstring('https://get.scoop.sh')
powershell scoop update
powershell scoop install neofetch
powershell scoop install curl

@REM Installing Oh-my-posh -> Oh-my-zsh
echo ====== Installing Oh-my-posh -> Oh-my-zsh (Linux) =======
powershell Set-ExecutionPolicy Bypass -Scope Process -Force; Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://ohmyposh.dev/install.ps1'))

@REM Installing PowerToys
echo ====== Installing PowerToys =======
powershell winget install Microsoft.PowerToys --source winget

@REM Installing tilling windo manager
echo ====== Installing GlazeWM (tilling window manager) =======
powershell curl -o %USERPROFILE%\windotfiles\GlazeWM\GlazeWM.exe https://github.com/lars-berger/GlazeWM/releases/download/v1.11.1/GlazeWM_x64_1.11.1.exe

@REM Pasting the start bat to the shell:startup
echo ====== Copying the start.bat file to the windows startup =======
powershell cp %USERPROFILE%\windotfiles\scripts\start.bat '%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\'