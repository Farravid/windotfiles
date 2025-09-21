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

###############################
# ALIASES
###############################

# Move and show the windotfiles folder
function windotfiles {Set-Location -Path $env:USERPROFILE\windotfiles && Get-ChildItem -Force }

###############################
# VISUAL CODE FOLDERS
###############################

# Open the windotfiles folder in Visual Studio Code
function cwindotfiles { Start-Process code $env:USERPROFILE\windotfiles -WindowStyle Hidden }