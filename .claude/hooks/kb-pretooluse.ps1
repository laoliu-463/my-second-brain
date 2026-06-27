$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$kbRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\.."))
$inputJson = [Console]::In.ReadToEnd()

function New-UnicodeString {
    param([int[]]$CodePoints)
    return -join ($CodePoints | ForEach-Object { [char]$_ })
}

$knowledgeDir = New-UnicodeString @(0x77E5, 0x8BC6, 0x5E93)

if ([string]::IsNullOrWhiteSpace($inputJson)) {
    exit 0
}

try {
    $event = $inputJson | ConvertFrom-Json
} catch {
    [Console]::Error.WriteLine("Blocked: hook input is not valid JSON.")
    exit 2
}

$toolName = [string]$event.tool_name
$toolInput = $event.tool_input

$filePath = ""
$command = ""

if ($null -ne $toolInput) {
    if ($toolInput.PSObject.Properties.Name -contains "file_path") {
        $filePath = [string]$toolInput.file_path
    } elseif ($toolInput.PSObject.Properties.Name -contains "path") {
        $filePath = [string]$toolInput.path
    }

    if ($toolInput.PSObject.Properties.Name -contains "command") {
        $command = [string]$toolInput.command
    }
}

function Normalize-PathText {
    param([string]$PathText)
    return (($PathText -replace "\\", "/") -replace "^\./", "")
}

function Resolve-AgentPath {
    param([string]$PathText)
    if ([string]::IsNullOrWhiteSpace($PathText)) { return "" }

    if ([System.IO.Path]::IsPathRooted($PathText)) {
        return [System.IO.Path]::GetFullPath($PathText)
    }

    return [System.IO.Path]::GetFullPath((Join-Path $kbRoot $PathText))
}

$normalizedFile = Normalize-PathText $filePath
$resolvedFile = Resolve-AgentPath $filePath
$normalizedResolved = Normalize-PathText $resolvedFile
$normalizedRoot = Normalize-PathText $kbRoot

function Test-PathUnder {
    param(
        [string]$PathText,
        [string]$RelativePrefix
    )
    $pathNorm = Normalize-PathText $PathText
    $rootNorm = Normalize-PathText (Join-Path $kbRoot $RelativePrefix)
    return ($pathNorm -eq $rootNorm -or $pathNorm.StartsWith("$rootNorm/"))
}

if ($normalizedFile -match "^\.obsidian/" -or (Test-PathUnder $resolvedFile ".obsidian")) {
    [Console]::Error.WriteLine("Blocked: .obsidian configuration must not be modified by agents.")
    exit 2
}

if ($toolName -match "^(Edit|MultiEdit)$" -and ($normalizedFile -match "^raw/" -or (Test-PathUnder $resolvedFile "raw"))) {
    [Console]::Error.WriteLine("Blocked: existing raw evidence is append-only. Add a new raw file or update the knowledge page original-link/source mapping instead.")
    exit 2
}

if ($toolName -eq "Write" -and ($normalizedFile -match "^raw/" -or (Test-PathUnder $resolvedFile "raw"))) {
    if ($resolvedFile -and (Test-Path -LiteralPath $resolvedFile)) {
        [Console]::Error.WriteLine("Blocked: Write would overwrite existing raw evidence.")
        exit 2
    }
}

if ($command -match "(?i)\b(Remove-Item|rm\s+-rf|del\s+|rmdir\s+)\b") {
    if ($command -match "(?i)(raw|\.obsidian|index\.md|log\.md)" -or $command.Contains($knowledgeDir)) {
        [Console]::Error.WriteLine("Blocked: destructive command targets protected knowledge-base paths.")
        exit 2
    }
}

exit 0
