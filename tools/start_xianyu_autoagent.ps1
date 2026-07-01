param(
  [switch]$Restart,
  [switch]$SkipApiCheck
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
    throw "未找到 XianyuAgent.py: $agentFile"
  }
  $content = Get-Content -LiteralPath $agentFile -Raw
  if ($content -match '<think>\.\*\?</think>') {
    return
  }
  $needle = '        """安全过滤模块"""'
  if (-not $content.Contains($needle)) {
    throw "无法定位 _safe_filter 插入点，请人工检查 XianyuAgent.py"
  }
  $insert = @'
        """安全过滤模块"""
        if not text:
            return text
        text = re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL | re.IGNORECASE).strip()
'@
  $content = $content.Replace($needle, $insert.TrimEnd())
  Set-Content -LiteralPath $agentFile -Value $content -Encoding UTF8
}

function Get-XianyuProcesses {
  param([string]$RepoPath)
  $venvPath = Join-Path $RepoPath ".venv"
  Get-CimInstance Win32_Process |
    Where-Object {
      $_.Name -match '^python(\.exe)?$' -and
      $_.CommandLine -like '*main.py*' -and
      (
        ($_.ExecutablePath -and $_.ExecutablePath.StartsWith($venvPath, [System.StringComparison]::OrdinalIgnoreCase)) -or
        ($_.CommandLine -like "*$RepoPath*")
      )
    }
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

  if ([string]::IsNullOrWhiteSpace($apiKey) -or $apiKey -match '默认使用|apikey|your|你的') {
    throw "API_KEY 未配置。请在 $repoPath\.env 填入 MiniMax Token Plan Subscription Key。"
  }
  if ([string]::IsNullOrWhiteSpace($cookie) -or $cookie.Length -lt 50 -or $cookie -notmatch '=') {
    throw "COOKIES_STR 未正确配置。请在 $repoPath\.env 填入闲鱼网页端完整 Cookie。"
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
      throw "MiniMax 连通性检查失败。请确认 Token Plan Key、seat/Credits 与 MODEL_BASE_URL。"
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
      Write-Host "XianyuAutoAgent 已在运行:"
      $existing | Select-Object ProcessId, ExecutablePath, CommandLine | Format-Table -AutoSize
      return
    }
  }

  New-Item -ItemType Directory -Force -Path "logs" | Out-Null
  $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
  $stdout = (Resolve-Path -LiteralPath "logs").Path + "\runtime-$stamp.out.log"
  $stderr = (Resolve-Path -LiteralPath "logs").Path + "\runtime-$stamp.err.log"

  $env:PYTHONUNBUFFERED = "1"
  $env:PYTHONUTF8 = "1"

  $process = Start-Process -FilePath $python -ArgumentList "-u", "main.py" -WorkingDirectory $repoPath -RedirectStandardOutput $stdout -RedirectStandardError $stderr -WindowStyle Hidden -PassThru
  Set-Content -LiteralPath (Join-Path "logs" "xianyuautoagent.pid") -Value $process.Id -Encoding ASCII
  Start-Sleep -Seconds 8

  $running = Get-CimInstance Win32_Process -Filter "ProcessId = $($process.Id)" -ErrorAction SilentlyContinue
  if (-not $running) {
    Write-Host "启动后进程已退出，最近错误日志:"
    if (Test-Path -LiteralPath $stderr) {
      Get-Content -LiteralPath $stderr -Tail 80
    }
    throw "XianyuAutoAgent 启动失败。"
  }

  Write-Host "XianyuAutoAgent 已启动。"
  Write-Host "PID: $($process.Id)"
  Write-Host "stderr: $stderr"
  Write-Host "stdout: $stdout"
  Write-Host "下一步: 用另一个闲鱼账号给商品发消息，确认自动回复。"
} finally {
  Pop-Location
}
