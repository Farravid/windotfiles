@REM Installing scoop, the 'non' command-line installer for Windows
@REM powershell iex (new-object net.webclient).downloadstring('https://get.scoop.sh')
@REM scoop update

@REM Installing scoop programs
@REM scoop install neofetch
@REM scoop install curl

@REM Installing winget programs
powershell winget install Microsoft.PowerToys --source winget

@REM Installing tilling windo manager
powershell curl -o .\GlazeWM\GlazeWM.exe https://github.com/lars-berger/GlazeWM/releases/download/v1.11.1/GlazeWM_x64_1.11.1.exe

@REM Pasting the start bat to the shell:startup
powershell cp .\start.bat '%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\' 