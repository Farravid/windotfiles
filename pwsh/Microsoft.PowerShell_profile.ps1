oh-my-posh init pwsh --config "$HOME/.cache/wal/posh-wal-clean.omp.json" | Invoke-Expression
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


###############################
# ALIASES
###############################

# Move and show the windotfiles folder
function windotfiles {Set-Location -Path $env:USERPROFILE\windotfiles && Get-ChildItem -Force }

# Open the windotfiles folder in Visual Studio Code
function cwindotfiles { code $env:USERPROFILE\windotfiles }

# Move and show the downloads folder
function down {Set-Location -Path $env:USERPROFILE\Downloads && Get-ChildItem -Force }

# Move and show the documents folder
function doc {Set-Location -Path $env:USERPROFILE\Documents && Get-ChildItem -Force }

# Launch the godot setup
Set-Alias -Name godot -Value $env:USERPROFILE\Documents\GitHub\ProjectoAmador\scripts\windows\launch_godot_editor.bat

# Adb for godot
function adbg {adb logcat -s godot}

# Open the windotfiles folder in Visual Studio Code
function cgodot { code $env:USERPROFILE\Documents\GitHub\ProjectoAmador }

# Update the terminal, glaze and dygma color scheme based on the given wallpaper
# It also sets the given wallpaper
function update-winwal ([string]$wallpaper) { python $env:USERPROFILE\windotfiles\scripts\colors\update_winwal.py $wallpaper }
