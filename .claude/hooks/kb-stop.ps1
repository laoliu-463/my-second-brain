$ErrorActionPreference = "Continue"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$kbRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\.."))
$validator = Join-Path $kbRoot "tools\kb_validate.ps1"

function New-UnicodeString {
    param([int[]]$CodePoints)
    return -join ($CodePoints | ForEach-Object { [char]$_ })
}

$knowledgeDir = New-UnicodeString @(0x77E5, 0x8BC6, 0x5E93)

function Test-GitRepo {
    $inside = git -C $kbRoot rev-parse --is-inside-work-tree 2>$null
    return ($LASTEXITCODE -eq 0 -and $inside -eq "true")
}

if (-not (Test-GitRepo)) {
    Write-Error "Blocked: cannot run Stop gate outside a git work tree."
    exit 2
}

$changed = git -C $kbRoot status --porcelain 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Blocked: unable to inspect git status."
    exit 2
}

if (-not $changed) {
    exit 0
}

$paths = @()
foreach ($line in $changed) {
    if ($line.Length -ge 4) {
        $paths += (($line.Substring(3)) -replace "\\", "/")
    }
}

$kbChanged = @($paths | Where-Object { $_.StartsWith("$knowledgeDir/") -or $_.StartsWith("raw/") })
$logChanged = @($paths | Where-Object { $_ -eq "log.md" })

if ($kbChanged.Count -gt 0 -and $logChanged.Count -eq 0) {
    Write-Error "Blocked: knowledge base changed but log.md was not updated."
    exit 2
}

powershell -NoProfile -ExecutionPolicy Bypass -File $validator -ChangedOnly
if ($LASTEXITCODE -ne 0) {
    Write-Error "Blocked: kb_validate.ps1 failed."
    exit 2
}

exit 0
