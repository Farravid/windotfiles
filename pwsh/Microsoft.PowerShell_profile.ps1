oh-my-posh init pwsh --config "$HOME/.cache/wal/posh-wal-clean.omp.json" | Invoke-Expression
Import-Module $env:USERPROFILE\windotfiles\\vendor\winwal\winwal.psm1

## ALIASES ##
Function dotfiles {Set-Location -Path $env:USERPROFILE\windotfiles && Get-ChildItem -Force }
Set-Alias -Name windotfiles -Value dotfiles