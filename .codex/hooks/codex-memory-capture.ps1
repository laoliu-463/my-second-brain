param(
    [ValidateSet("UserPromptSubmit", "Stop")]
    [string]$EventName = "Stop",

    [switch]$NoCloud
)

$ErrorActionPreference = "Stop"

function Write-CodexMemoryStatus {
    param([string]$Message)
    [Console]::Error.WriteLine("[codex-memory] $Message")
}

try {
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [Console]::InputEncoding = $utf8NoBom
    [Console]::OutputEncoding = $utf8NoBom

    $projectRoot = "D:\Docs\Books\my second brain"
    $eventText = [Console]::In.ReadToEnd()
    if ([string]::IsNullOrWhiteSpace($eventText)) {
        $eventText = "{}"
    }

    $event = $null
    try {
        $event = $eventText | ConvertFrom-Json -ErrorAction Stop
    } catch {
        $event = $null
    }

    $cwd = $null
    if ($null -ne $event) {
        foreach ($name in @("cwd", "current_working_directory", "working_directory", "workspace_root", "workspaceRoot", "project_root", "projectRoot")) {
            if ($event.PSObject.Properties.Name -contains $name) {
                $value = $event.$name
                if ($value) {
                    $cwd = [string]$value
                    break
                }
            }
        }
    }
    if (-not $cwd) {
        $cwd = (Get-Location).Path
    }

    $resolvedProject = [System.IO.Path]::GetFullPath($projectRoot).TrimEnd("\")
    $resolvedCwd = [System.IO.Path]::GetFullPath($cwd).TrimEnd("\")
    $projectPrefix = "$resolvedProject\"
    if (
        -not $resolvedCwd.Equals($resolvedProject, [StringComparison]::OrdinalIgnoreCase) -and
        -not $resolvedCwd.StartsWith($projectPrefix, [StringComparison]::OrdinalIgnoreCase)
    ) {
        exit 0
    }

    $captureScript = Join-Path $resolvedProject "tools\memory_capture.py"
    if (-not (Test-Path -LiteralPath $captureScript)) {
        Write-CodexMemoryStatus "missing $captureScript"
        exit 0
    }

    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCommand) {
        $pythonCommand = Get-Command py -ErrorAction SilentlyContinue
    }
    if (-not $pythonCommand) {
        Write-CodexMemoryStatus "python executable not found"
        exit 0
    }
    $python = $pythonCommand.Source

    $source = if ($EventName -eq "UserPromptSubmit") { "codex-user-prompt-submit" } else { "codex-stop" }
    $captureId = "codex-$($EventName.ToLowerInvariant())-$(Get-Date -Format 'yyyyMMddHHmmssfff')"
    $captureArgs = @(
        $captureScript,
        "--agent", "codex",
        "--source", $source,
        "--session-id", "codex-current-project",
        "--everos-session-id", "my-second-brain-codex",
        "--encoding", "utf-8",
        "--input-format", "codex-hook-json",
        "--capture-id", $captureId
    )
    if ($NoCloud) {
        $captureArgs += "--no-cloud"
    }

    $tempEventPath = Join-Path ([System.IO.Path]::GetTempPath()) "codex-memory-$([guid]::NewGuid().ToString('N')).json"
    [System.IO.File]::WriteAllText($tempEventPath, $eventText, $utf8NoBom)
    try {
        & $python @captureArgs --input-file $tempEventPath
    } finally {
        if (Test-Path -LiteralPath $tempEventPath) {
            Remove-Item -LiteralPath $tempEventPath -Force
        }
    }

    if ($LASTEXITCODE -ne 0) {
        Write-CodexMemoryStatus "memory_capture exited with code $LASTEXITCODE"
        exit 0
    }
} catch {
    Write-CodexMemoryStatus $_.Exception.Message
    exit 0
}

exit 0
