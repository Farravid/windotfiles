oh-my-posh init pwsh --config "$HOME/.cache/wal/posh-wal-clean.omp.json" | Invoke-Expression
Import-Module $env:USERPROFILE\windotfiles\\vendor\winwal\winwal.psm1

###############################
# ALIASES
###############################

# Move and show the windotfiles folder
function windotfiles {Set-Location -Path $env:USERPROFILE\windotfiles && Get-ChildItem -Force }

# Launch the godot setup
Set-Alias -Name godot -Value $env:USERPROFILE\Documents\GitHub\ProjectoAmador\scripts\windows\launch_godot_editor.bat

# Update the terminal, glaze and dygma color scheme based on the given wallpaper
# It also sets the given wallpaper
function update-winwal ([string]$wallpaper) { python $env:USERPROFILE\windotfiles\scripts\common.py $wallpaper }