# Builds the local GlazeWM fork and overwrites the winget-installed exes in place.
# Run from anywhere; edit $Repo if the checkout moves.
$ErrorActionPreference = 'Stop'
$Repo    = "$HOME\glazewm"
$Install = 'C:\Program Files\glzr.io\GlazeWM'

Write-Host 'Building release...' -ForegroundColor Cyan
cargo build --release --manifest-path "$Repo\Cargo.toml"

Write-Host 'Stopping GlazeWM...' -ForegroundColor Cyan
glazewm command wm-exit 2>$null
# ponytail: fixed wait for the exe lock to release; bump if a copy ever fails.
Start-Sleep -Seconds 2

$rel = "$Repo\target\release"
# ponytail: only wm + wm-cli. The workspace's default-members excludes wm-watcher
# so `cargo build` never produces it, AND the PR never touches it -> the stock
# watcher is already identical. If the PR ever modifies wm-watcher, build it with
# `cargo build --release -p wm-watcher` and add it back here (also stop the
# running glazewm-watcher.exe first, since it locks its own exe).
$copies = @(
  @{ src = "$rel\glazewm.exe";     dst = "$Install\glazewm.exe" }
  @{ src = "$rel\glazewm-cli.exe"; dst = "$Install\cli\glazewm.exe" }
)

# Copying into Program Files needs admin -> run the copies in an elevated child.
$copyScript = ($copies | ForEach-Object {
  "Copy-Item -LiteralPath '$($_.src)' -Destination '$($_.dst)' -Force"
}) -join '; '
Write-Host 'Copying exes (elevating)...' -ForegroundColor Cyan
Start-Process powershell -Verb RunAs -Wait -ArgumentList @(
  '-NoProfile','-Command',$copyScript
)

Write-Host 'Restarting GlazeWM...' -ForegroundColor Cyan
Start-Process glazewm
Write-Host 'Done.' -ForegroundColor Green
