param(
    [string]$Agent = "codex",
    [string]$SessionId = "",
    [string]$CommandLine = "",
    [switch]$NoCloud,
    [switch]$FailOnCloudError,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AgentCommand
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$kbRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir ".."))
$captureScript = Join-Path $kbRoot "tools\memory_capture.py"

if (-not (Test-Path -LiteralPath $captureScript)) {
    throw "memory_capture.py not found: $captureScript"
}

if (-not $SessionId) {
    $SessionId = "my-second-brain-$Agent"
}

if ($AgentCommand.Count -gt 0 -and $AgentCommand[0] -eq "--") {
    if ($AgentCommand.Count -eq 1) {
        $AgentCommand = @()
    } else {
        $AgentCommand = $AgentCommand[1..($AgentCommand.Count - 1)]
    }
}

if (-not $CommandLine -and $AgentCommand.Count -eq 0) {
    throw "Provide -CommandLine or a command to wrap, for example: powershell -File tools\agent_memory_wrapper.ps1 -Agent codex -CommandLine `"codex`""
}

$day = Get-Date -Format "yyyyMMdd"
$safeAgent = ($Agent.ToLowerInvariant() -replace "[^a-z0-9_.-]+", "-")
$transcriptDir = Join-Path $kbRoot "tmp\agent-memory-transcripts\$day\$safeAgent"
New-Item -ItemType Directory -Force -Path $transcriptDir | Out-Null

$stamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$transcriptPath = Join-Path $transcriptDir "$stamp.wrapper.transcript.txt"
$exitCode = 0

Start-Transcript -LiteralPath $transcriptPath -Force | Out-Null
try {
    if ($CommandLine) {
        cmd.exe /d /s /c $CommandLine
    } else {
        & $AgentCommand[0] @($AgentCommand | Select-Object -Skip 1)
    }
    $exitCode = $LASTEXITCODE
    if ($null -eq $exitCode) { $exitCode = 0 }
} catch {
    $exitCode = 1
    Write-Error $_
} finally {
    Stop-Transcript | Out-Null
}

$captureArgs = @(
    $captureScript,
    "--agent", $Agent,
    "--source", "agent-wrapper",
    "--session-id", $SessionId,
    "--input-file", $transcriptPath
)

if ($NoCloud) {
    $captureArgs += "--no-cloud"
}
if ($FailOnCloudError) {
    $captureArgs += "--fail-on-cloud-error"
}

python @captureArgs
exit $exitCode
