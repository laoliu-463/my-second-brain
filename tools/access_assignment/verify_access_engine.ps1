param(
    [string]$AccdbPath = "D:\Docs\Books\my second brain\tmp\access_assignment_output\Access作业-机自250X-张某某_数据查询版.accdb"
)

$ErrorActionPreference = "Stop"

function Remove-ComObject {
    param([object]$ComObject)
    if ($null -ne $ComObject) {
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($ComObject)
    }
}

if (-not (Test-Path -LiteralPath $AccdbPath)) {
    throw "ACCDB not found: $AccdbPath"
}

$dao = New-Object -ComObject DAO.DBEngine.120
$database = $null

try {
    $database = $dao.OpenDatabase($AccdbPath)

    $tableRecordset = $database.OpenRecordset("SELECT COUNT(*) AS 总数 FROM [人员信息表]")
    $rowCount = $tableRecordset.Fields("总数").Value
    $tableRecordset.Close()

    $queryNames = @("地区表", "单位表", "科室表", "性别表", "民族表", "学历表", "政治面貌表")
    $results = @()
    foreach ($name in $queryNames) {
        $recordset = $database.OpenRecordset("SELECT COUNT(*) AS 总数 FROM [$name]")
        $results += [PSCustomObject]@{
            QueryName = $name
            RowCount  = $recordset.Fields("总数").Value
        }
        $recordset.Close()
    }

    $sample = $database.OpenRecordset(@"
SELECT TOP 5 [姓名], [单位], [科室]
FROM [人员信息表]
WHERE [区名]='淮水区' AND [性别]='男'
ORDER BY [序号]
"@)
    $sampleRows = @()
    while (-not $sample.EOF) {
        $sampleRows += [PSCustomObject]@{
            姓名 = $sample.Fields("姓名").Value
            单位 = $sample.Fields("单位").Value
            科室 = $sample.Fields("科室").Value
        }
        $sample.MoveNext()
    }
    $sample.Close()

    if ($rowCount -ne 200) {
        throw "人员信息表行数异常，期望 200，实际 $rowCount"
    }

    Write-Output "TABLE_ROWS=$rowCount"
    $results | Sort-Object QueryName | Format-Table -AutoSize | Out-String | Write-Output
    $sampleRows | Format-Table -AutoSize | Out-String | Write-Output
    Write-Output "VERIFY_OK"
} finally {
    if ($database) { $database.Close() }
    Remove-ComObject $database
    Remove-ComObject $dao
}
