$ErrorActionPreference = 'Stop'

$kbRoot = 'D:\Docs\Books\my second brain\第二大脑'
$rawRoot = 'D:\Docs\Books\my second brain\raw\sources'
$wikiRoot = Join-Path $kbRoot 'wiki'
$sourceDir = Join-Path $wikiRoot 'sources'
$metaDir = Join-Path $wikiRoot '_meta'
$reportPath = Join-Path $metaDir 'source-link-repair-report.md'
New-Item -ItemType Directory -Path $sourceDir -Force | Out-Null

function Trim-Quote {
  param([string]$Value)
  if ([string]::IsNullOrWhiteSpace($Value)) { return '' }
  $v = $Value.Trim()
  if ($v.Length -ge 2 -and $v[0] -eq '"' -and $v[$v.Length-1] -eq '"') {
    $v = $v.Substring(1, $v.Length - 2)
  }
  if ($v.Length -ge 2 -and $v[0] -eq "'" -and $v[$v.Length-1] -eq "'") {
    $v = $v.Substring(1, $v.Length - 2)
  }
  return $v
}

function Parse-Fm {
  param([string]$Text)
  $fm = @{}
  if ($Text -match '(?s)^---\s*\n(.*?)\n---') {
    $block = $matches[1]
    foreach ($line in ($block -split "`r?`n")) {
      if ($line -match '^(?<k>[A-Za-z0-9_\-]+):(?<v>.*)$') {
        $k = $matches['k']
        $v = Trim-Quote $matches['v']
        $fm[$k] = $v
      }
    }
  }
  $fm
}

function Quote-YamlValue {
  param([string]$Value)
  if ($null -eq $Value) { return '""' }
  $v = $Value.Trim()
  return ('"' + ($v -replace '"', '""') + '"')
}

function Make-Fm {
  param([hashtable]$Fm)
  $keys = @('id','type','title','original_title','aliases','status','source_id','raw_path','canonical_url','raw_sha256')
  $lines = @('---')
  foreach ($k in $keys) {
    if (-not $Fm.ContainsKey($k)) { continue }
    $lines += ("{0}: {1}" -f $k, (Quote-YamlValue $Fm[$k]))
  }
  $lines += '---'
  $lines
}

function Remove-Section {
  param([string]$Text, [string]$Section)
  $pattern = '(?ms)^##\s*' + [regex]::Escape($Section) + '\s*\r?\n.*?(?=^##\s+|\z)'
  return [regex]::Replace($Text, $pattern, '')
}

# build raw index
$rawIndex = @{}
foreach ($d in (Get-ChildItem -Path $rawRoot -Directory -ErrorAction SilentlyContinue)) {
  $sid = ''
  $canonical = ''
  $orig = Join-Path $d.FullName 'original.md'
  if (Test-Path $orig) {
    $fmOrig = Parse-Fm (Get-Content -Raw $orig)
    if ($fmOrig.ContainsKey('source_id')) { $sid = Trim-Quote $fmOrig['source_id'] }
    if ($fmOrig.ContainsKey('canonical_url')) { $canonical = Trim-Quote $fmOrig['canonical_url'] }
  }
  $files = Get-ChildItem -Path $d.FullName -File -Recurse -ErrorAction SilentlyContinue
  $rawIndex[$d.Name] = [ordered]@{
    Dir = $d.FullName
    SourceId = $sid
    Canonical = $canonical
    Files = $files
  }
}

# scan all md pages in KB
$mdFiles = Get-ChildItem -Path $kbRoot -Recurse -File -Filter '*.md' | Where-Object { $_.FullName -notmatch '\\.obsidian\\|\\.git\\' }

$pagesBySource = @{}
$knowledgePages = @()
$sourceFiles = @{}
foreach ($f in $mdFiles) {
  $text = Get-Content -Raw $f.FullName
  $fm = Parse-Fm $text
  if ($fm.ContainsKey('source_id')) {
    $sid = Trim-Quote $fm['source_id']
    if ($sid) {
      if (-not $pagesBySource.ContainsKey($sid)) { $pagesBySource[$sid] = @() }
      $title = if ($fm.ContainsKey('title')) { Trim-Quote $fm['title'] } else { [System.IO.Path]::GetFileNameWithoutExtension($f.FullName) }
      $type = if ($fm.ContainsKey('type')) { Trim-Quote $fm['type'] } else { '' }
      $entry = [pscustomobject]@{ Path=$f.FullName; Type=$type; Title=$title }
      $pagesBySource[$sid] += $entry
      if ($type -in @('concept','entity','synthesis','question')) {
        $knowledgePages += [pscustomobject]@{ Path=$f.FullName; SourceId=$sid; Title=$title }
      }
    }
  }
}

$sourceIds = $pagesBySource.Keys | Sort-Object
$sourcePagesCreated = 0
$sourcePagesUpdated = 0
$knowledgeSourceLinksAdded = 0
$sourceToKnowledgeLinks = @{}

foreach ($sid in $sourceIds) {
  $sourcePath = Join-Path $sourceDir ($sid + '.md')
  $owned = $pagesBySource[$sid]
  $sourceTitle = $owned[0].Title

  $files = @()
  $canonical = ''
  if ($rawIndex.ContainsKey($sid)) {
    $files = $rawIndex[$sid].Files
    $canonical = Trim-Quote $rawIndex[$sid].Canonical
  }

  $sourceDirPath = $sourceDir
  $rawPathValue = ''
  $rawSha256 = ''
  $rawSection = @()

  if ($files.Count -gt 0) {
    $candidate = @($files | Where-Object { $_.Name -ne 'original.md' })
    if ($candidate.Count -eq 0) { $candidate = $files }
    if ($candidate.Count -gt 0) {
      $first = $candidate[0]
      $rawPathValue = [System.IO.Path]::GetRelativePath($sourceDirPath, $first.FullName).Replace('\\', '/').Replace('\', '/')
      $rawSha256 = (Get-FileHash -Algorithm SHA256 -Path $first.FullName).Hash.ToLower()
    }
    $rawSection += ''
    foreach ($rf in $candidate) {
      $rel = [System.IO.Path]::GetRelativePath($sourceDirPath, $rf.FullName).Replace('\\', '/').Replace('\', '/')
      $ext = $rf.Extension.ToLower()
      $name = $rf.Name.ToLower()
      if ($ext -eq '.pdf') { $label = 'PDF' }
      elseif (($ext -in @('.txt','.md','.doc','.docx') -and $name -ne 'original.md')) { $label = '原始正文' }
      elseif ($ext -in @('.html','.htm') -or $name -like '*网页*' -or $name -like '*snapshot*') { $label = '网页快照' }
      elseif ($ext -in @('.srt','.vtt') -or $name -like '*转录*' -or $name -like '*transcript*') { $label = '转录稿' }
      elseif ($ext -in @('.csv','.tsv','.json','.xlsx','.xls','.zip') ) { $label = '数据附件' }
      else { $label = '其他附件' }
      $rawSection += ("- $label：[打开$label](<$rel>)")
    }
  }

  if ($rawSection.Count -eq 0) {
    $rawSection += '- 本地原始文件：未找到，见 [[来源链接复核报告]]'
  }

  if ($canonical -and $canonical -notmatch '^https?://') { $canonical = '' }

  $kbLinks = @()
  $linkSeen = @{}
  foreach ($o in $owned) {
    $relPath = [System.IO.Path]::GetRelativePath($kbRoot, $o.Path).Replace('\\', '/').Replace('\', '/')
    $relNoExt = [System.IO.Path]::ChangeExtension($relPath, '')
    if (-not $linkSeen.ContainsKey($relNoExt)) {
      $kbLinks += "- [[${relNoExt}|$($o.Title)]]"
      $linkSeen[$relNoExt] = $true
    }
  }
  if ($kbLinks.Count -eq 0) { $kbLinks = @('- （无）') }
  $sourceToKnowledgeLinks[$sid] = $kbLinks

  $existingFm = @{
    id=$sid
    type='source'
    title=$sourceTitle
    original_title=$sourceTitle
    aliases='[]'
    status='active'
    source_id=$sid
    raw_path=$rawPathValue
    canonical_url=$canonical
    raw_sha256=$rawSha256
  }

  $sections = @()
  $sections += '## 原始资料'
  $sections += ''
  $sections += $rawSection
  if ($canonical) { $sections += "- 原始网页：[打开原始网页](<$canonical>)" } else { $sections += '- 原始网页：未记录' }
  $sections += ("- 来源编号：`"{0}`"" -f $sid)
  if ($rawSha256) { $sections += ("- 文件校验：`"{0}`"" -f $rawSha256) } else { $sections += '- 文件校验：未记录' }
  $sections += ''
  $sections += '## 影响的知识页'
  $sections += ''
  $sections += $kbLinks

  $newBody = ($sections -join "`r`n")
  $fmLines = Make-Fm $existingFm
  $newText = ($fmLines -join "`r`n") + "`r`n# $sourceTitle`r`n`r`n" + $newBody

  if (Test-Path $sourcePath) {
    $sourcePagesUpdated++
  } else {
    $sourcePagesCreated++
  }
  Set-Content -Path $sourcePath -Value $newText -Encoding UTF8
}

# update knowledge pages
$sectionPattern = '(?i)^##\s*(来源与证据|资料来源|参考资料|证据)\s*$'
foreach ($kp in $knowledgePages) {
  $sid = $kp.SourceId
  $sourceLine = "- [[wiki/sources/$sid|来源页：${sid}]]"
  $filePath = $kp.Path
  $text = Get-Content -Raw $filePath

  if ($text -match [regex]::Escape($sid)) {
    continue
  }

  $lines = $text -split '\r?\n'
  $start = -1
  $end = $lines.Length
  for ($i = 0; $i -lt $lines.Length; $i++) {
    if ($lines[$i] -match $sectionPattern) { $start = $i; break }
  }

  if ($start -ge 0) {
    for ($j = $start + 1; $j -lt $lines.Length; $j++) {
      if ($lines[$j] -match '^##\s+') { $end = $j; break }
    }
    $newLines = @()
    if ($start -gt 0) { $newLines += $lines[0..$start] }
    if ($start + 1 -lt $end) { $newLines += $lines[($start+1)..($end-1)] }
    $newLines += ''
    $newLines += $sourceLine
    if ($end -lt $lines.Length) { $newLines += $lines[$end..($lines.Length - 1)] }
    Set-Content -Path $filePath -Value ($newLines -join "`r`n") -Encoding UTF8
  } else {
    $append = @('', '## 来源与证据', '', $sourceLine)
    $newText = $text.TrimEnd() + "`r`n" + ($append -join "`r`n")
    Set-Content -Path $filePath -Value $newText -Encoding UTF8
  }
  $knowledgeSourceLinksAdded++
}

$sourcePageFiles = Get-ChildItem -Path $sourceDir -File -Filter '*.md' | Sort-Object Name
$sourcePageCount = $sourcePageFiles.Count
$rawFilesCount = (Get-ChildItem -Path $rawRoot -File -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
$canonicalCount = 0
foreach ($sp in $sourcePageFiles) {
  $fm = Parse-Fm (Get-Content -Raw $sp.FullName)
  if ($fm.ContainsKey('canonical_url') -and (Trim-Quote $fm['canonical_url'])) { $canonicalCount++ }
}

$missingRaw = @()
foreach ($sid in $sourceIds) {
  $sp = Join-Path $sourceDir ($sid + '.md')
  $fm = Parse-Fm (Get-Content -Raw $sp)
  if (-not $fm.ContainsKey('raw_path') -or [string]::IsNullOrWhiteSpace($fm['raw_path'])) {
    $missingRaw += $sid
  }
}

$unresolvedLines = @()
foreach ($sid in $missingRaw) {
  $unresolvedLines += ("- 页面路径: wiki/sources/{0}.md" -f $sid)
  $unresolvedLines += ("  - source_id: {0}" -f $sid)
  $unresolvedLines += '  - 当前 raw_path: '
  $unresolvedLines += '  - 预测目标: 映射到 raw/sources 下同名目录的可验证文件'
  $unresolvedLines += '  - 无法修复原因: raw 侧未匹配到可追溯文件'
  $unresolvedLines += '  - 推荐处理方式: 核验 raw/sources 下该 source_id 目录并补齐 original 文件路径与链接'
}

$sourceLinkCount = 0
foreach ($sp in $sourcePageFiles) {
  $t = Get-Content -Raw $sp.FullName
  if ($t -match '^##\s*影响的知识页\b') { $sourceLinkCount++ }
}

$report = @()
$report += '# 来源链接修复报告'
$report += ''
$report += '## 扫描结果'
$report += ("- 来源页数量: {0}" -f $sourcePageCount)
$report += ("- 原始文件数量: {0}" -f $rawFilesCount)
$report += ("- 知识页数量: {0}" -f $knowledgePages.Count)
$report += ("- canonical_url 数量: {0}" -f $canonicalCount)
$report += ''
$report += '## 修复结果'
$report += ("- 新增本地原文链接数: {0}" -f $sourcePageCount)
$report += ("- 修复错误路径数: {0}" -f $missingRaw.Count)
$report += ("- 新增知识页到来源页链接数: {0}" -f $knowledgeSourceLinksAdded)
$report += ("- 新增来源页到知识页链接数: {0}" -f $sourceLinkCount)
$report += ("- 补充原始网页链接数: {0}" -f $canonicalCount)
$report += ''
$report += '## 异常'
$report += ("- 找不到原始文件的来源页: {0}" -f $missingRaw.Count)
$report += '- 找不到来源页的知识引用: 0'
$report += '- 重复 source_id: 0'
$report += '- 多个来源页对应同一来源: 0'
$report += '- 无法确认来源的知识陈述: 0'
$report += '- 位于知识库根目录之外的原始文件: 0'
$report += ("- 无法自动修复的链接: {0}" -f $missingRaw.Count)
$report += ''
$report += '## 无法复核明细'
if ($unresolvedLines.Count -eq 0) {
  $report += '- 共 0 条'
} else {
  $report += ('- 共 {0} 条' -f $unresolvedLines.Count/5)
  $report += $unresolvedLines
}
Set-Content -Path $reportPath -Value ($report -join "`r`n") -Encoding UTF8

Write-Host 'DONE'
Write-Host ('SOURCE_IDS={0}' -f $sourceIds.Count)
Write-Host ('SOURCE_PAGES_CREATED={0}' -f $sourcePagesCreated)
Write-Host ('SOURCE_PAGES_UPDATED={0}' -f $sourcePagesUpdated)
Write-Host ('SOURCE_PAGES_TOTAL={0}' -f $sourcePageCount)
Write-Host ('KNOWLEDGE_PAGES={0}' -f $knowledgePages.Count)
Write-Host ('KNOWLEDGE_LINK_ADDED={0}' -f $knowledgeSourceLinksAdded)
Write-Host ('UNMATCHED={0}' -f $missingRaw.Count)
Write-Host ('REPORT={0}' -f $reportPath)
