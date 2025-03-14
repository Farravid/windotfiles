oh-my-posh init pwsh --config "$HOME/.cache/wal/posh-wal-atomic.omp.json" | Invoke-Expression
Import-Module $env:USERPROFILE\windotfiles\\vendor\winwal\winwal.psm1

###############################
# FUNCTIONS
###############################
<#
 Change the audio output device to the next one
#>
function change_audio_output 
{
    $Audio = Get-AudioDevice -playback
    Write-Output "Audio device was " $Audio.Name
    Write-Output "Audio device now set to " 

    if ($Audio.Index -EQ 1) {
    (Get-AudioDevice -list | Where-Object Index -EQ 2 | Set-AudioDevice).Name
    }  Else {
    (Get-AudioDevice -list | Where-Object Index -EQ 1 | Set-AudioDevice).Name
    }
}

<#
 Copy the current computer flow launcher settings to the windotfiles
 Flow launcher doesn't support SYMLINKS! 
#>

function cp_fl_to_windotfiles 
{
    Copy-Item  $env:Appdata\FlowLauncher\Plugins $env:USERPROFILE\windotfiles\flow_launcher -Force -Recurse
    Copy-Item  $env:Appdata\FlowLauncher\Settings $env:USERPROFILE\windotfiles\flow_launcher -Force -Recurse
    Copy-Item  $env:Appdata\FlowLauncher\Themes $env:USERPROFILE\windotfiles\flow_launcher -Force -Recurse
}

<#
 Copy the current windotfiles flow launcher settings to computer
 Flow launcher doesn't support SYMLINKS! 
#>

function cp_windotfiles_to_fl 
{
    Copy-Item  $env:USERPROFILE\windotfiles\flow_launcher\Plugins $env:Appdata\FlowLauncher -Force -Recurse
    Copy-Item  $env:USERPROFILE\windotfiles\flow_launcher\Settings $env:Appdata\FlowLauncher -Force -Recurse
    Copy-Item  $env:USERPROFILE\windotfiles\flow_launcher\Themes $env:Appdata\FlowLauncher -Force -Recurse
    Start-Process $env:LocalAppData\FlowLauncher\Flow.Launcher.exe
}


###############################
# ALIASES
###############################

# Move and show the windotfiles folder
function windotfiles {Set-Location -Path $env:USERPROFILE\windotfiles && Get-ChildItem -Force }

# Move and show the downloads folder
function down {Set-Location -Path $env:USERPROFILE\Downloads && Get-ChildItem -Force }

# Move and show the documents folder
function doc {Set-Location -Path $env:USERPROFILE\Documents && Get-ChildItem -Force }

# Launch the godot setup
Set-Alias -Name godot -Value $env:USERPROFILE\Documents\GitHub\ProjectoAmador\scripts\windows\launch_godot_editor.bat

# Adb for godot
function adbg {adb logcat -s godot}

# Updat the windotfiles packages
function update-windotfiles { python $env:USERPROFILE\windotfiles\scripts\update.py }

#Launch the startup script
function startup { python $env:USERPROFILE\windotfiles\scripts\startup.py }

###############################
# VISUAL CODE FOLDERS
###############################

# Open the windotfiles folder in Visual Studio Code
function cwindotfiles { Start-Process code $env:USERPROFILE\windotfiles -WindowStyle Hidden }

# Open the windotfiles folder in Visual Studio Code
function cgodot { Start-Process code $env:USERPROFILE\Documents\GitHub\ProjectoAmador -WindowStyle Hidden }

# Open the farrapiler folder in Visual Studio Code
function cfarrapiler { Start-Process code $env:USERPROFILE\Documents\GitHub\farrapiler -WindowStyle Hidden }

# Open the HPC folder in Visual Studio Code
function chpc { Start-Process code \\wsl.localhost\Manjaro\home\Farravid\repos\HPC -WindowStyle Hidden }