param(
    [switch]$ChangedOnly
)

$ErrorActionPreference = "Continue"
$script:failed = $false
$script:warningCount = 0

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$KbRoot = [System.IO.Path]::GetFullPath((Join-Path $ScriptDir ".."))

function New-UnicodeString {
    param([int[]]$CodePoints)
    return -join ($CodePoints | ForEach-Object { [char]$_ })
}

$KnowledgeDir = New-UnicodeString @(0x77E5, 0x8BC6, 0x5E93)
$SourceMappingDir = "90-" + (New-UnicodeString @(0x6765, 0x6E90, 0x4E0E, 0x6620, 0x5C04))
$CognitiveFolder = "05-" + (New-UnicodeString @(0x8BA4, 0x77E5, 0x4E0E, 0x6210, 0x957F))
$AgentFolder = "05-" + (New-UnicodeString @(0x667A, 0x80FD, 0x4F53, 0x4E0E)) + "Agent" + (New-UnicodeString @(0x4F53, 0x7CFB))
$OriginalLinkHeading = New-UnicodeString @(0x539F, 0x6587, 0x94FE, 0x63A5)

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

function Get-RelativeRepoPath {
    param([string]$FullPath)

    try {
        return [System.IO.Path]::GetRelativePath($KbRoot, $FullPath)
    } catch {
        $rootFull = [System.IO.Path]::GetFullPath($KbRoot)
        $fileFull = [System.IO.Path]::GetFullPath($FullPath)
        $rootUriText = $rootFull
        if (-not $rootUriText.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
            $rootUriText += [System.IO.Path]::DirectorySeparatorChar
        }
        $rootUri = New-Object System.Uri($rootUriText)
        $fileUri = New-Object System.Uri($fileFull)
        return [System.Uri]::UnescapeDataString($rootUri.MakeRelativeUri($fileUri).ToString()).Replace("/", [System.IO.Path]::DirectorySeparatorChar)
    }
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
            Normalize-RepoPath (Get-RelativeRepoPath $_.FullName)
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
    if (-not $RepoPath.StartsWith("$KnowledgeDir/")) { return $false }
    if ($RepoPath -match ("^" + [regex]::Escape($KnowledgeDir) + "/(_review|_meta|sources|" + [regex]::Escape($SourceMappingDir) + ")(/|$)")) { return $false }
    return ($RepoPath -match '\.md$')
}

function Get-FrontMatterScalar {
    param(
        [string]$Text,
        [string]$Key
    )
    if ($Text -notmatch "(?s)^\s*---\s*\r?\n(.*?)\r?\n---") { return $null }
    $block = $matches[1]
    $pattern = "(?m)^\s*$([regex]::Escape($Key))\s*:\s*(.+?)\s*$"
    if ($block -match $pattern) {
        return $matches[1].Trim().Trim('"').Trim("'")
    }
    return $null
}

function Get-OriginalLinkSection {
    param([string]$Text)
    $heading = [regex]::Escape($OriginalLinkHeading)
    $match = [regex]::Match($Text, "(?ms)^##\s*$heading\s*\r?\n(?<body>.*?)(?=^##\s+|\z)")
    if ($match.Success) { return $match.Groups["body"].Value }
    return $null
}

function Get-RawSourceWikiTargets {
    param([string]$Text)
    if ([string]::IsNullOrWhiteSpace($Text)) { return @() }
    $matches = [regex]::Matches($Text, '\[\[\s*(raw/sources/[^\]\|#]+)(?:#[^\]\|]+)?(?:\|[^\]]+)?\]\]')
    $targets = @()
    foreach ($match in $matches) {
        $targets += $match.Groups[1].Value.Trim()
    }
    return @($targets | Where-Object { $_ } | Sort-Object -Unique)
}

function Test-RawSourceTargetExists {
    param([string]$Target)
    $pathText = ($Target -replace "/", [System.IO.Path]::DirectorySeparatorChar)
    $fullPath = Join-Path $KbRoot $pathText
    return (Test-Path -LiteralPath $fullPath -PathType Leaf)
}

function Test-KnowledgeMarkdownPage {
    param([string]$RepoPath)
    return ($RepoPath.StartsWith("$KnowledgeDir/") -and $RepoPath.EndsWith(".md"))
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

$kbOrRawChanged = @($files | Where-Object { $_.StartsWith("$KnowledgeDir/") -or $_.StartsWith("raw/") })
$logChanged = @($files | Where-Object { $_ -eq "log.md" })

if ($kbOrRawChanged.Count -gt 0 -and $logChanged.Count -eq 0) {
    Write-Fail "Changes under knowledge or raw paths require updating log.md"
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
        if ($text -notmatch '(?m)^\s*(updated_at|updated)\s*:') {
            Write-Fail "Formal knowledge page lacks updated_at or updated: $file"
        }

        $sourceLevel = Get-FrontMatterScalar -Text $text -Key "source_level"
        $sourceExempt = ($sourceLevel -and $sourceLevel.Trim().ToLowerInvariant() -eq "none")
        if (-not $sourceExempt) {
            $originalSection = Get-OriginalLinkSection -Text $text
            $rawTargets = Get-RawSourceWikiTargets -Text $originalSection
            if ($rawTargets.Count -eq 0) {
                Write-Fail "Formal page must have a ## $OriginalLinkHeading section with a raw/sources WikiLink: $file"
            } else {
                foreach ($target in $rawTargets) {
                    if (-not (Test-RawSourceTargetExists -Target $target)) {
                        Write-Fail "Formal page raw source link does not resolve: $file => $target"
                    }
                }
            }
        }
    }
}

$cognitivePath = Join-Path (Join-Path $KbRoot $KnowledgeDir) $CognitiveFolder
$agentPath = Join-Path (Join-Path $KbRoot $KnowledgeDir) $AgentFolder
if ((Test-Path -LiteralPath $cognitivePath) -and (Test-Path -LiteralPath $agentPath)) {
    Write-Warn "Two 05-* folders exist by design. Do not rename them without explicit approval."
}

if ($script:failed) {
    exit 1
}

Write-Host "KB validation passed. Checked $($files.Count) file(s), warnings: $script:warningCount." -ForegroundColor Green
exit 0
