$ClaudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME ".claude" }

# Different profiles (.claude-personal vs .claude-work) have laid out the ponytail
# marketplace checkout at different depths; check both known locations.
$PonytailScript = ""
foreach ($candidate in @("plugins\marketplaces\ponytail\hooks\ponytail-statusline.ps1",
                         "plugins\plugins\marketplaces\ponytail\hooks\ponytail-statusline.ps1")) {
    $path = Join-Path $ClaudeDir $candidate
    if (Test-Path $path) {
        $PonytailScript = $path
        break
    }
}

$StdinJson = [Console]::In.ReadToEnd()

$ModelName = ""
$Effort = ""
$Cwd = ""
try {
    $Data = $StdinJson | ConvertFrom-Json -ErrorAction Stop
    if ($Data.model -and $Data.model.display_name) {
        $ModelName = $Data.model.display_name
    }
    if ($Data.effort -and $Data.effort.level) {
        $Effort = $Data.effort.level
    }
    if ($Data.workspace -and $Data.workspace.current_dir) {
        $Cwd = $Data.workspace.current_dir
    } elseif ($Data.cwd) {
        $Cwd = $Data.cwd
    }
} catch {
    # Leave $ModelName/$Effort/$Cwd empty if JSON parsing fails
}

$Account = ""
try {
    $ConfigJsonPath = Join-Path $ClaudeDir ".claude.json"
    $Account = (Get-Content $ConfigJsonPath -Raw -ErrorAction Stop | ConvertFrom-Json -ErrorAction Stop).oauthAccount.emailAddress
} catch {
    # Leave $Account empty if the file/field is missing
}

$Esc = [char]27
$InfoParts = @()
if ($Account) {
    $InfoParts += "${Esc}[38;5;109m$Account${Esc}[0m"
}
if ($Cwd) {
    $InfoParts += "${Esc}[38;5;180m$Cwd${Esc}[0m"
}
if ($ModelName) {
    $InfoParts += "${Esc}[38;5;250m$ModelName${Esc}[0m"
}
if ($Effort) {
    $InfoParts += "${Esc}[38;5;244m[$($Effort.ToUpperInvariant())]${Esc}[0m"
}
$InfoStr = $InfoParts -join " "

$PonytailOutput = ""
if (Test-Path $PonytailScript) {
    try {
        $PonytailOutput = ($StdinJson | & powershell -NoProfile -ExecutionPolicy Bypass -File $PonytailScript) -join "`n"
    } catch {
        $PonytailOutput = ""
    }
}

if ($InfoStr -and $PonytailOutput) {
    [Console]::Write("$InfoStr $PonytailOutput")
} else {
    [Console]::Write("$InfoStr$PonytailOutput")
}
