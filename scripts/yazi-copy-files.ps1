# Copies the given file(s) to the Windows clipboard as real file objects
# (CF_HDROP) plus a "Preferred DropEffect" hint. `Set-Clipboard -LiteralPath`
# alone only writes CF_HDROP, which Explorer/email accept but Electron/Chromium
# apps (WhatsApp, Slack, Discord, Teams...) silently reject as "no content" -
# they require the DropEffect format to treat the drop as a copy.
param(
    [Parameter(Mandatory, ValueFromRemainingArguments)]
    [string[]]$Path
)

Add-Type -AssemblyName System.Windows.Forms

$files = New-Object System.Collections.Specialized.StringCollection
foreach ($p in $Path) {
    $files.Add((Resolve-Path -LiteralPath $p).Path) | Out-Null
}

$data = New-Object System.Windows.Forms.DataObject
$data.SetFileDropList($files)

# DROPEFFECT_COPY = 1, as a little-endian 32-bit int stream.
$dropEffect = New-Object System.IO.MemoryStream
$dropEffect.Write([BitConverter]::GetBytes([int]1), 0, 4)
$data.SetData("Preferred DropEffect", $dropEffect)

[System.Windows.Forms.Clipboard]::SetDataObject($data, $true)
