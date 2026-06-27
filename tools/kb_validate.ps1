param(
    [switch]$ChangedOnly
)

$ErrorActionPreference = "Continue"
$script:failed = $false
$script:warningCount = 0

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$KbRoot = [System.IO.Path]::GetFullPath((Join-Path $ScriptDir ".."))

function Write-Fail {
    param([string]$Message)
    Write-Host "KB_VALIDATION_ERROR: $Message" -ForegroundColor Red
    $script:failed = $true
}

function Write-Warn {
    param([string]$Message)
    Write-Host "KB_VALIDATION_WARNING: $Message" -ForegroundColor Yellow
    $script:warningCount++
}

function Test-GitRepo {
    $inside = git -C $KbRoot rev-parse --is-inside-work-tree 2>$null
    return ($LASTEXITCODE -eq 0 -and $inside -eq "true")
}

function Normalize-RepoPath {
    param([string]$Path)
    return ($Path -replace "\\", "/").Trim()
}

function Get-ChangedFiles {
    $files = New-Object System.Collections.Generic.HashSet[string]

    $commands = @(
        @("diff", "--name-only"),
        @("diff", "--cached", "--name-only"),
        @("ls-files", "--others", "--exclude-standard")
    )

    foreach ($args in $commands) {
        $output = git -C $KbRoot @args 2>$null
        if ($LASTEXITCODE -ne 0) { continue }
        foreach ($line in $output) {
            $path = Normalize-RepoPath $line
            if ($path) { [void]$files.Add($path) }
        }
    }

    return @($files)
}

function Get-AllMarkdownFiles {
    Get-ChildItem -LiteralPath $KbRoot -Recurse -File -Filter "*.md" |
        Where-Object {
            $full = $_.FullName
            $full -notmatch "\\\.git\\" -and
            $full -notmatch "\\tmp\\" -and
            $full -notmatch "\\\.obsidian\\"
        } |
        ForEach-Object {
            Normalize-RepoPath ([System.IO.Path]::GetRelativePath($KbRoot, $_.FullName))
        }
}

function Get-FileText {
    param([string]$RepoPath)
    $fullPath = Join-Path $KbRoot ($RepoPath -replace "/", [System.IO.Path]::DirectorySeparatorChar)
    if (-not (Test-Path -LiteralPath $fullPath)) { return $null }
    return Get-Content -LiteralPath $fullPath -Raw
}

function Test-HasFrontmatter {
    param([string]$Text)
    return ($Text -match "(?s)^\s*---\s*\r?\n.*?\r?\n---")
}

function Test-FormalKnowledgePage {
    param([string]$RepoPath)
    if ($RepoPath -notmatch "^知识库/") { return $false }
    if ($RepoPath -match "^知识库/(_review|_meta|sources|90-来源与映射)(/|$)") { return $false }
    return ($RepoPath -match "\.md$")
}

function Test-KnowledgeMarkdownPage {
    param([string]$RepoPath)
    return ($RepoPath -match "^知识库/.*\.md$")
}

$isGitRepo = Test-GitRepo

if ($ChangedOnly -and -not $isGitRepo) {
    Write-Fail "-ChangedOnly requires a git work tree. Run without -ChangedOnly for a full markdown scan."
    exit 1
}

$files = if ($ChangedOnly) { Get-ChangedFiles } else { Get-AllMarkdownFiles }
$files = @($files | Where-Object { $_ } | Sort-Object -Unique)

if ($ChangedOnly -and $files.Count -eq 0) {
    Write-Host "KB validation passed. No changed files detected." -ForegroundColor Green
    exit 0
}

if ($isGitRepo) {
    $rawStatus = git -C $KbRoot status --porcelain -- raw 2>$null
    foreach ($line in $rawStatus) {
        if ($line.Length -lt 3) { continue }
        $status = $line.Substring(0, 2)
        $path = Normalize-RepoPath $line.Substring(3)
        if ($status -match "M|D|R") {
            Write-Fail "raw evidence must be append-only: $status $path"
        }
    }
} elseif (-not $ChangedOnly) {
    Write-Warn "Not a git work tree; raw append-only checks are limited during full scan."
}

$kbOrRawChanged = @($files | Where-Object { $_ -match "^(知识库|raw)/" })
$logChanged = @($files | Where-Object { $_ -eq "log.md" })

if ($kbOrRawChanged.Count -gt 0 -and $logChanged.Count -eq 0) {
    Write-Fail "Changes under 知识库/ or raw/ require updating log.md"
}

foreach ($file in $files) {
    if (-not (Test-KnowledgeMarkdownPage $file)) { continue }

    $text = Get-FileText $file
    if ($null -eq $text) { continue }

    if (-not (Test-HasFrontmatter $text)) {
        Write-Fail "Knowledge markdown page lacks YAML frontmatter: $file"
        continue
    }

    if (Test-FormalKnowledgePage $file) {
        if ($text -notmatch "(?m)^\s*(updated_at|updated)\s*:") {
            Write-Fail "Formal knowledge page lacks updated_at or updated: $file"
        }

        $hasSource = (
            $text -match "(?m)^\s*sources\s*:" -or
            $text -match "(?m)^\s*raw_evidence\s*:" -or
            $text -match "(?m)^\s*source_level\s*:\s*none\s*$"
        )
        if (-not $hasSource) {
            Write-Fail "Formal page must have sources, raw_evidence, or source_level: none: $file"
        }
    }
}

$cognitivePath = Join-Path $KbRoot "知识库\05-认知与成长"
$agentPath = Join-Path $KbRoot "知识库\05-智能体与Agent体系"
if ((Test-Path -LiteralPath $cognitivePath) -and (Test-Path -LiteralPath $agentPath)) {
    Write-Warn "Two 05-* folders exist by design. Do not rename them without explicit approval."
}

if ($script:failed) {
    exit 1
}

Write-Host "KB validation passed. Checked $($files.Count) file(s), warnings: $script:warningCount." -ForegroundColor Green
exit 0
