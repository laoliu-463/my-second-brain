param(
  [switch]$Restart,
  [switch]$SkipApiCheck,
  [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$repoPath = Join-Path $root "tmp\external\XianyuAutoAgent"
$repoUrl = "https://github.com/shaxiu/XianyuAutoAgent.git"

function Read-DotEnv {
  param([string]$Path)
  $map = @{}
  if (-not (Test-Path -LiteralPath $Path)) {
    return $map
  }
  Get-Content -LiteralPath $Path | ForEach-Object {
    if ($_ -match '^\s*([^#=]+)=(.*)$') {
      $map[$matches[1].Trim()] = $matches[2].Trim()
    }
  }
  return $map
}

function Unquote-EnvValue {
  param([string]$Value)
  if ($null -eq $Value) {
    return ""
  }
  $trimmed = $Value.Trim()
  if (($trimmed.StartsWith('"') -and $trimmed.EndsWith('"')) -or ($trimmed.StartsWith("'") -and $trimmed.EndsWith("'"))) {
    return $trimmed.Substring(1, $trimmed.Length - 2)
  }
  return $trimmed
}

function Set-DotEnvValue {
  param(
    [string]$Path,
    [string]$Key,
    [string]$Value
  )
  $lines = @()
  if (Test-Path -LiteralPath $Path) {
    $lines = @(Get-Content -LiteralPath $Path)
  }
  $seen = $false
  $updated = foreach ($line in $lines) {
    if ($line -match "^\s*$([regex]::Escape($Key))\s*=") {
      $seen = $true
      "$Key=$Value"
    } else {
      $line
    }
  }
  if (-not $seen) {
    $updated += "$Key=$Value"
  }
  Set-Content -LiteralPath $Path -Value $updated -Encoding UTF8
}

function Ensure-ThinkFilter {
  param([string]$RepoPath)
  $agentFile = Join-Path $RepoPath "XianyuAgent.py"
  if (-not (Test-Path -LiteralPath $agentFile)) {
    throw "XianyuAgent.py not found: $agentFile"
  }
  $content = Get-Content -LiteralPath $agentFile -Raw
  if ($content -match '<think>\.\*\?</think>') {
    return
  }
  $needle = '        blocked_phrases = ['
  if (-not $content.Contains($needle)) {
    throw "Cannot locate _safe_filter insertion point in XianyuAgent.py"
  }
  $insert = @'
        if not text:
            return text
        text = re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL | re.IGNORECASE).strip()
        blocked_phrases = [
'@
  $content = $content.Replace($needle, $insert.TrimEnd())
  Set-Content -LiteralPath $agentFile -Value $content -Encoding UTF8
}

function Get-XianyuProcesses {
  param([string]$RepoPath)
  $venvPath = Join-Path $RepoPath ".venv"
  $pidFile = Join-Path $RepoPath "logs\xianyuautoagent.pid"
  $knownPidProcesses = @()
  if (Test-Path -LiteralPath $pidFile) {
    $knownPid = (Get-Content -LiteralPath $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1)
    if ($knownPid -match '^\d+$') {
      $knownPidProcesses = @(Get-CimInstance Win32_Process -Filter "ProcessId = $knownPid" -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '^python(\.exe)?$' -and $_.CommandLine -like '*main.py*' })
    }
  }
  $queryProcesses = @(Get-CimInstance Win32_Process |
    Where-Object {
      $_.Name -match '^python(\.exe)?$' -and
      $_.CommandLine -like '*main.py*' -and
      (
        ($_.ExecutablePath -and $_.ExecutablePath.StartsWith($venvPath, [System.StringComparison]::OrdinalIgnoreCase)) -or
        ($_.CommandLine -like "*$RepoPath*")
      )
    })
  @($knownPidProcesses + $queryProcesses) | Sort-Object ProcessId -Unique
}

if (-not (Test-Path -LiteralPath $repoPath)) {
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $repoPath) | Out-Null
  git clone $repoUrl $repoPath
}

Push-Location $repoPath
try {
  if (-not (Test-Path -LiteralPath ".env")) {
    if (Test-Path -LiteralPath ".env.example") {
      Copy-Item -LiteralPath ".env.example" -Destination ".env"
    } else {
      New-Item -ItemType File -Path ".env" | Out-Null
    }
  }

  Set-DotEnvValue -Path ".env" -Key "MODEL_BASE_URL" -Value "https://api.minimaxi.com/v1"
  Set-DotEnvValue -Path ".env" -Key "MODEL_NAME" -Value "MiniMax-M3"

  $envMap = Read-DotEnv -Path ".env"
  $apiKey = Unquote-EnvValue $envMap["API_KEY"]
  $cookie = Unquote-EnvValue $envMap["COOKIES_STR"]

  if ([string]::IsNullOrWhiteSpace($apiKey) -or $apiKey -match 'apikey|your|API_KEY') {
    throw "API_KEY is not configured. Fill MiniMax Token Plan Subscription Key in $repoPath\.env."
  }
  if ([string]::IsNullOrWhiteSpace($cookie) -or $cookie.Length -lt 50 -or $cookie -notmatch '=') {
    throw "COOKIES_STR is not configured correctly. Fill the full goofish web Cookie in $repoPath\.env."
  }

  if (-not (Test-Path -LiteralPath ".venv\Scripts\python.exe")) {
    py -3 -m venv .venv
  }
  $python = (Resolve-Path -LiteralPath ".venv\Scripts\python.exe").Path

  & $python -c "import openai, websockets, loguru, dotenv, requests" 2>$null
  if ($LASTEXITCODE -ne 0) {
    & $python -m pip install -U pip
    & $python -m pip install -r requirements.txt
  }

  Ensure-ThinkFilter -RepoPath $repoPath

  if (-not $SkipApiCheck) {
    try {
      Invoke-WebRequest -Uri "https://api.minimaxi.com/v1/models" -Headers @{ Authorization = "Bearer $apiKey" } -Method Get -TimeoutSec 20 | Out-Null
    } catch {
      throw "MiniMax connectivity check failed. Verify Token Plan Key, seat/Credits, and MODEL_BASE_URL."
    }
  }

  $existing = @(Get-XianyuProcesses -RepoPath $repoPath)
  if ($existing.Count -gt 0) {
    if ($Restart) {
      foreach ($proc in $existing) {
        Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
      }
      Start-Sleep -Seconds 2
    } else {
      Write-Host "XianyuAutoAgent is already running:"
      $existing | Select-Object ProcessId, ExecutablePath, CommandLine | Format-Table -AutoSize
      return
    }
  }

  if ($CheckOnly) {
    Write-Host "XianyuAutoAgent preflight check passed."
    Write-Host "Project path: $repoPath"
    return
  }

  New-Item -ItemType Directory -Force -Path "logs" | Out-Null
  $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
  $stdout = (Resolve-Path -LiteralPath "logs").Path + "\runtime-$stamp.out.log"
  $stderr = (Resolve-Path -LiteralPath "logs").Path + "\runtime-$stamp.err.log"

  $env:PYTHONUNBUFFERED = "1"
  $env:PYTHONUTF8 = "1"

  $mainPath = Join-Path $repoPath "main.py"
  $process = Start-Process -FilePath $python -ArgumentList "-u", $mainPath -WorkingDirectory $repoPath -RedirectStandardOutput $stdout -RedirectStandardError $stderr -WindowStyle Hidden -PassThru
  Set-Content -LiteralPath (Join-Path "logs" "xianyuautoagent.pid") -Value $process.Id -Encoding ASCII
  Start-Sleep -Seconds 8

  $running = Get-CimInstance Win32_Process -Filter "ProcessId = $($process.Id)" -ErrorAction SilentlyContinue
  if (-not $running) {
    Write-Host "Process exited after startup. Recent stderr log:"
    if (Test-Path -LiteralPath $stderr) {
      Get-Content -LiteralPath $stderr -Tail 80
    }
    throw "XianyuAutoAgent startup failed."
  }

  Write-Host "XianyuAutoAgent started."
  Write-Host "PID: $($process.Id)"
  Write-Host "stderr: $stderr"
  Write-Host "stdout: $stdout"
  Write-Host "Next step: send a test message from another goofish account and confirm auto-reply."
} finally {
  Pop-Location
}
