param(
    [string]$KbRoot = "D:\Docs\Books\my second brain",
    [string]$ReportDir = "D:\Docs\Books\my second brain\06-报告证据\日报"
)

$ErrorActionPreference = "Stop"

function Resolve-PathSafe {
    param([string]$Path)
    try {
        return [System.IO.Path]::GetFullPath((Resolve-Path -LiteralPath $Path -ErrorAction Stop).ProviderPath)
    } catch {
        return $null
    }
}

function Get-FrontMatterValue {
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

function Test-FormalKnowledgePage {
    param([string]$RelativePath)
    if (-not $RelativePath.StartsWith("知识库/")) { return $false }
    if ($RelativePath -match '^知识库/(_review|_meta|sources|90-来源与映射)(/|$)') { return $false }
    return $RelativePath.EndsWith(".md")
}

function Get-OriginalLinkSection {
    param([string]$Text)
    $match = [regex]::Match($Text, "(?ms)^##\s*原文链接\s*\r?\n(?<body>.*?)(?=^##\s+|\z)")
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

function Test-VaultRelativeFileExists {
    param([string]$RelativePath)
    $pathText = ($RelativePath -replace "/", [System.IO.Path]::DirectorySeparatorChar)
    $fullPath = Join-Path $kbPath $pathText
    return (Test-Path -LiteralPath $fullPath -PathType Leaf)
}

function Add-Section {
    param(
        [System.Text.StringBuilder]$Builder,
        [string]$Title,
        [array]$Items
    )
    [void]$Builder.AppendLine("## $Title")
    if ($Items.Count -eq 0) {
        [void]$Builder.AppendLine("- 无")
        return
    }
    foreach ($line in $Items) {
        [void]$Builder.AppendLine("- $line")
    }
}

if (-not (Test-Path -LiteralPath $KbRoot)) {
    throw "KB 根目录不存在：$KbRoot"
}

$kbPath = Resolve-PathSafe $KbRoot
$rawPath = Join-Path $kbPath "raw"
$knowledgePath = Join-Path $kbPath "知识库"
$inboxPath = Join-Path $kbPath "00-收集箱"
$mailboxPath = Join-Path $kbPath "00-收件箱"
$indexPath = Join-Path $kbPath "index.md"
$logPath = Join-Path $kbPath "log.md"
$sourcesPath = Join-Path $knowledgePath "sources"
$entitiesPath = Join-Path $knowledgePath "entities"
$conceptsPath = Join-Path $knowledgePath "concepts"
$synthesesPath = Join-Path $knowledgePath "syntheses"

New-Item -ItemType Directory -Path $ReportDir -Force | Out-Null
$runAt = Get-Date
$stamp = $runAt.ToString("yyyyMMdd-HHmmss")
$date = $runAt.ToString("yyyy-MM-dd")
$reportPath = Join-Path $ReportDir ("daily-maintenance-$stamp.md")

$issues = [System.Collections.Generic.List[PSObject]]::new()
$stats = @{
    "目录项检查数" = 0
    "知识页扫描数" = 0
    "WikiLink缺失" = 0
    "Markdown链接缺失" = 0
    "原文链接区块缺失" = 0
    "raw原文目标缺失" = 0
    "canonical_url异常" = 0
    "Frontmatter缺失" = 0
}

$required = @(
    @{Name = "raw"; Path = $rawPath},
    @{Name = "知识库"; Path = $knowledgePath},
    @{Name = "index.md"; Path = $indexPath},
    @{Name = "00-收集箱"; Path = $inboxPath},
    @{Name = "00-收件箱"; Path = $mailboxPath}
)

foreach ($item in $required) {
    if (-not (Test-Path -LiteralPath $item.Path)) {
        $issues.Add([PSCustomObject]@{
            Severity = "ERROR"
            Area = "目录检查"
            Message = "缺失关键路径：$($item.Name) ($($item.Path))"
            Suggest = "请确认根目录结构是否完整"
        })
    }
}

if (-not (Test-Path -LiteralPath $knowledgePath)) {
    $stats["知识页扫描数"] = 0
} else {
    $wikiFiles = Get-ChildItem -LiteralPath $knowledgePath -Recurse -File -Filter "*.md"
    $stats["知识页扫描数"] = $wikiFiles.Count

    $relMap = @{}
    $nameMap = @{}
    foreach ($f in $wikiFiles) {
        $rel = [System.IO.Path]::GetRelativePath($kbPath, $f.FullName).Replace("\", "/")
        $relNoExt = [System.IO.Path]::ChangeExtension($rel, $null).Replace("\", "/")
        $relWithExt = $rel
        $relMap[$rel] = $f.FullName
        $relMap["$relNoExt.md"] = $f.FullName
        $relMap[$relNoExt] = $f.FullName
        $base = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
        if (-not $nameMap.ContainsKey($base)) { $nameMap[$base] = @() }
        $nameMap[$base] += $f.FullName
    }

    foreach ($f in $wikiFiles) {
        $text = Get-Content -LiteralPath $f.FullName -Raw
        $relative = [System.IO.Path]::GetRelativePath($kbPath, $f.FullName).Replace("\", "/")
        $stats["目录项检查数"]++

        if (-not ($text -match "(?s)^\s*---\s*\r?\n(.*?)\r?\n---")) {
            $stats["Frontmatter缺失"]++
            $issues.Add([PSCustomObject]@{
                Severity = "WARN"
                Area = "frontmatter"
                Message = "缺少 frontmatter：$relative"
                Suggest = "补充至少 title 和 updated，保持规范字段"
            })
        }

        if (Test-FormalKnowledgePage -RelativePath $relative) {
            $sourceLevel = Get-FrontMatterValue -Text $text -Key "source_level"
            $sourceExempt = ($sourceLevel -and $sourceLevel.Trim().ToLowerInvariant() -eq "none")
            if (-not $sourceExempt) {
                $originalSection = Get-OriginalLinkSection -Text $text
                $rawTargetsInOriginalSection = Get-RawSourceWikiTargets -Text $originalSection
                if ($rawTargetsInOriginalSection.Count -eq 0) {
                    $stats["原文链接区块缺失"]++
                    $issues.Add([PSCustomObject]@{
                        Severity = "WARN"
                        Area = "原文链接"
                        Message = "正式知识页缺少可点击 raw 原文链接区块：$relative"
                        Suggest = "添加 ## 原文链接，并用 Obsidian WikiLink 直接指向真实存在的 raw/sources 原文附件"
                    })
                }
            }
        }

        $wikiLinkPattern = '\[\[([^\]\n#|]+)(?:#[^\]\n]+)?(?:\|[^\]\n]+)?\]\]'
        $wikiMatches = [regex]::Matches($text, $wikiLinkPattern)
        foreach ($m in $wikiMatches) {
            $targetRaw = $m.Groups[1].Value.Trim()
            if ($targetRaw -match '^(https?|mailto):') { continue }
            if ($targetRaw.StartsWith("raw/sources/")) {
                if (-not (Test-VaultRelativeFileExists -RelativePath $targetRaw)) {
                    $stats["raw原文目标缺失"]++
                    $issues.Add([PSCustomObject]@{
                        Severity = "WARN"
                        Area = "原文链接"
                        Message = "raw 原文链接无法命中：$relative => $targetRaw"
                        Suggest = "确认 raw/sources 下真实文件名，修正链接；文件确实缺失时写入待核查报告，不要新建 source 页冒充"
                    })
                }
                continue
            }
            $target = $targetRaw
            if ($target.Contains("#")) { $target = $target -replace '#.*$' }
            $found = $false
            if ($target.Contains("/")) {
                if ($target -notmatch '\.md$') { $target = "$target.md" }
                if ($relMap.ContainsKey($target) -or $relMap.ContainsKey("知识库/$target")) {
                    $found = $true
                }
            } else {
                if ($nameMap.ContainsKey($target) -and $nameMap[$target].Count -ge 1) {
                    $found = $true
                }
            }
            if (-not $found) {
                $stats["WikiLink缺失"]++
                $issues.Add([PSCustomObject]@{
                    Severity = "WARN"
                    Area = "WikiLink"
                    Message = "页面链接可能失效：$relative => $targetRaw"
                    Suggest = "确认目标页路径或更新为有效 wiki link"
                })
            }
        }

        $mdLinkPattern = '(?<!\!)\[[^\]]+\]\(([^)\s]+)\)'
        $mdMatches = [regex]::Matches($text, $mdLinkPattern)
        foreach ($m in $mdMatches) {
            $linkRaw = $m.Groups[1].Value.Trim()
            if ($linkRaw -match '^(https?|mailto|file):') { continue }
            if ($linkRaw -match '^#') { continue }
            $link = $linkRaw -replace '#.*$'
            if ($link -eq '') { continue }

            $isAbsolutePath = [System.IO.Path]::IsPathRooted($link)
            $candidate = if ($isAbsolutePath) { $link } else { Join-Path $f.DirectoryName $link }
            if (-not (Test-Path -LiteralPath $candidate)) {
                $stats["Markdown链接缺失"]++
                $issues.Add([PSCustomObject]@{
                    Severity = "WARN"
                    Area = "Markdown链接"
                    Message = "相对链接可能失效：$relative => $linkRaw"
                    Suggest = "修复为可定位的本地路径或放弃该引用"
                })
            }
        }
    }

    if (Test-Path -LiteralPath $sourcesPath) {
        $sourcePages = Get-ChildItem -LiteralPath $sourcesPath -Filter "*.md" -File
        foreach ($sp in $sourcePages) {
            $sText = Get-Content -LiteralPath $sp.FullName -Raw
            $canonical = Get-FrontMatterValue -Text $sText -Key "canonical_url"
            if ($canonical -and $canonical -notmatch '^https?://') {
                $stats["canonical_url异常"]++
                $issues.Add([PSCustomObject]@{
                    Severity = "WARN"
                    Area = "来源映射"
                    Message = "canonical_url 非标准URL：$([System.IO.Path]::GetRelativePath($kbPath, $sp.FullName).Replace('\','/')) => $canonical"
                    Suggest = "保留合法 URL 或记录为 未记录"
                })
            }
        }
    }
}

$collector = @(
    "KB 根目录: $kbPath",
    "执行时间: $($runAt.ToString('yyyy-MM-dd HH:mm:ss'))"
)

$rawCount = if (Test-Path -LiteralPath (Join-Path $rawPath 'sources')) {
    (Get-ChildItem -LiteralPath (Join-Path $rawPath 'sources') -Recurse -File).Count
} else {
    0
}

$inboxCount = if (Test-Path -LiteralPath $inboxPath) { (Get-ChildItem -LiteralPath $inboxPath -Recurse -File).Count } else { 0 }
$mailboxCount = if (Test-Path -LiteralPath $mailboxPath) { (Get-ChildItem -LiteralPath $mailboxPath -Recurse -File).Count } else { 0 }

$builder = New-Object System.Text.StringBuilder
[void]$builder.AppendLine("# 每日知识库规范维护报告")
[void]$builder.AppendLine("")
[void]$builder.AppendLine("## 执行信息")
foreach ($line in $collector) {
    [void]$builder.AppendLine("- $line")
}
[void]$builder.AppendLine("")
[void]$builder.AppendLine("## 关键指标")
[void]$builder.AppendLine("- 知识页扫描数：$($stats["知识页扫描数"])")
[void]$builder.AppendLine("- raw/sources 文件数：$rawCount")
[void]$builder.AppendLine("- 00-收集箱 文件数：$inboxCount")
[void]$builder.AppendLine("- 00-收件箱 文件数：$mailboxCount")
[void]$builder.AppendLine("- 缺失 WikiLink 数：$($stats["WikiLink缺失"])")
[void]$builder.AppendLine("- 缺失 Markdown 链接数：$($stats["Markdown链接缺失"])")
[void]$builder.AppendLine("- 原文链接区块缺失数：$($stats["原文链接区块缺失"])")
[void]$builder.AppendLine("- raw 原文目标缺失数：$($stats["raw原文目标缺失"])")
[void]$builder.AppendLine("- canonical_url 异常数：$($stats["canonical_url异常"])")
[void]$builder.AppendLine("- frontmatter 缺失数：$($stats["Frontmatter缺失"])")
[void]$builder.AppendLine("")

Add-Section -Builder $builder -Title "本次问题清单" -Items @()

if ($issues.Count -eq 0) {
    [void]$builder.AppendLine("- 无")
} else {
    $grouped = $issues | Group-Object Severity
    foreach ($g in $grouped) {
        [void]$builder.AppendLine("")
        [void]$builder.AppendLine("### $($g.Name) ($($g.Count))")
        foreach ($i in $g.Group) {
            [void]$builder.AppendLine("- [${($i.Severity)}] $($i.Area): $($i.Message)")
            [void]$builder.AppendLine("  - 建议：$($i.Suggest)")
        }
    }
}

[void]$builder.AppendLine("")
[void]$builder.AppendLine("## 建议动作")
if ($issues.Count -eq 0) {
    [void]$builder.AppendLine("- 当前通过基础巡检，可进入常规 ingest/query/lint 周期。")
} else {
    [void]$builder.AppendLine("- 优先处理 WARN/ERROR 问题清单中的链接与来源映射。")
    [void]$builder.AppendLine("- 对高风险误报场景，先通过专题人工确认后再批量修复。")
}

Set-Content -LiteralPath $reportPath -Value $builder.ToString() -Encoding UTF8

if (-not (Test-Path -LiteralPath $logPath)) {
    Set-Content -LiteralPath $logPath -Value @(
        "# log.md",
        "",
        "## [YYYY-MM-DD] lint | 日志",
        "- 按任务创建时系统自动写入占位条目"
    ) -Encoding UTF8
}

$logTitle = "## [$date] lint | 每日知识库维护"
$logBody = @(
    $logTitle,
    "",
    "- 执行脚本: daily_kb_maintenance.ps1",
    "- 执行时间: $($runAt.ToString('HH:mm:ss'))",
    "- 知识页扫描数: $($stats["知识页扫描数"])",
    "- 缺失 WikiLink: $($stats["WikiLink缺失"])",
    "- 缺失 Markdown 链接: $($stats["Markdown链接缺失"])",
    "- 原文链接区块缺失: $($stats["原文链接区块缺失"])",
    "- raw 原文目标缺失: $($stats["raw原文目标缺失"])",
    "- canonical_url 异常: $($stats["canonical_url异常"])",
    "- frontmatter缺失: $($stats["Frontmatter缺失"])",
    ""
) -join "`r`n"

Add-Content -LiteralPath $logPath -Value $logBody

Write-Host "DONE: $reportPath"
Write-Host "issues=$($issues.Count)"
Write-Host "wikiLinks=$($stats["WikiLink缺失"]) mdLinks=$($stats["Markdown链接缺失"]) rawMissing=$($stats["raw原文目标缺失"]) originalSections=$($stats["原文链接区块缺失"])"
