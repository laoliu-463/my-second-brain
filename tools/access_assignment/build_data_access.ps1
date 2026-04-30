param(
    [string]$SourceXls = "D:\Docs\Books\my second brain\tmp\access_assignment_output\source.xls",
    [string]$OutputAccdb = "D:\Docs\Books\my second brain\tmp\access_assignment_output\Access作业-机自250X-张某某_数据查询版.accdb"
)

$ErrorActionPreference = "Stop"

function Remove-ComObject {
    param([object]$ComObject)
    if ($null -ne $ComObject) {
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($ComObject)
    }
}

function New-AccessDatabase {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path) {
        Remove-Item -LiteralPath $Path -Force
    }
    $catalog = New-Object -ComObject ADOX.Catalog
    try {
        [void]$catalog.Create("Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$Path;Jet OLEDB:Engine Type=6;")
    } finally {
        Remove-ComObject $catalog
    }
}

function Add-QueryDef {
    param(
        [object]$Database,
        [string]$Name,
        [string]$Sql
    )

    try {
        $Database.QueryDefs.Delete($Name)
    } catch {
    }
    [void]$Database.CreateQueryDef($Name, $Sql)
}

if (-not (Test-Path -LiteralPath $SourceXls)) {
    throw "Source XLS not found: $SourceXls"
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutputAccdb) | Out-Null
New-AccessDatabase -Path $OutputAccdb

$connection = New-Object System.Data.OleDb.OleDbConnection("Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$OutputAccdb")
$excel = $null
$workbook = $null
$worksheet = $null
$usedRange = $null
$dao = $null
$database = $null

try {
    $connection.Open()

    $createSql = @"
CREATE TABLE [人员信息表] (
    [序号] INTEGER NOT NULL,
    [城市] TEXT(50),
    [区名] TEXT(50),
    [单位] TEXT(50),
    [科室] TEXT(100),
    [姓名] TEXT(50),
    [年龄] INTEGER,
    [性别] TEXT(10),
    [籍贯] TEXT(100),
    [民族] TEXT(20),
    [出生年月] DATETIME,
    [身份证号] TEXT(30),
    [学历] TEXT(20),
    [职务] TEXT(50),
    [政治面貌] TEXT(20)
)
"@
    $command = $connection.CreateCommand()
    $command.CommandText = $createSql
    [void]$command.ExecuteNonQuery()

    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $workbook = $excel.Workbooks.Open($SourceXls)
    $worksheet = $workbook.Worksheets.Item(1)
    $usedRange = $worksheet.UsedRange

    for ($row = 2; $row -le $usedRange.Rows.Count; $row++) {
        $sequence = [int]$usedRange.Item($row, 1).Value2
        if ($sequence -le 0) {
            continue
        }

        $birthdayCell = $usedRange.Item($row, 11).Value2
        $birthday = $null
        if ($null -ne $birthdayCell -and $birthdayCell.ToString().Trim() -ne "") {
            $birthday = [DateTime]::FromOADate([double]$birthdayCell)
        }

        $insert = $connection.CreateCommand()
        $insert.CommandText = @"
INSERT INTO [人员信息表]
([序号],[城市],[区名],[单位],[科室],[姓名],[年龄],[性别],[籍贯],[民族],[出生年月],[身份证号],[学历],[职务],[政治面貌])
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
"@

        $values = @(
            @{ Type = [System.Data.OleDb.OleDbType]::Integer; Value = $sequence },
            @{ Type = [System.Data.OleDb.OleDbType]::VarWChar; Value = $usedRange.Item($row, 2).Text.ToString().Trim() },
            @{ Type = [System.Data.OleDb.OleDbType]::VarWChar; Value = $usedRange.Item($row, 3).Text.ToString().Trim() },
            @{ Type = [System.Data.OleDb.OleDbType]::VarWChar; Value = $usedRange.Item($row, 4).Text.ToString().Trim() },
            @{ Type = [System.Data.OleDb.OleDbType]::VarWChar; Value = $usedRange.Item($row, 5).Text.ToString().Trim() },
            @{ Type = [System.Data.OleDb.OleDbType]::VarWChar; Value = $usedRange.Item($row, 6).Text.ToString().Trim() },
            @{ Type = [System.Data.OleDb.OleDbType]::Integer; Value = [int]$usedRange.Item($row, 7).Value2 },
            @{ Type = [System.Data.OleDb.OleDbType]::VarWChar; Value = $usedRange.Item($row, 8).Text.ToString().Trim() },
            @{ Type = [System.Data.OleDb.OleDbType]::VarWChar; Value = $usedRange.Item($row, 9).Text.ToString().Trim() },
            @{ Type = [System.Data.OleDb.OleDbType]::VarWChar; Value = $usedRange.Item($row, 10).Text.ToString().Trim() },
            @{ Type = [System.Data.OleDb.OleDbType]::DBTimeStamp; Value = $(if ($birthday) { $birthday } else { [DBNull]::Value }) },
            @{ Type = [System.Data.OleDb.OleDbType]::VarWChar; Value = $usedRange.Item($row, 12).Text.ToString().Trim() },
            @{ Type = [System.Data.OleDb.OleDbType]::VarWChar; Value = $usedRange.Item($row, 13).Text.ToString().Trim() },
            @{ Type = [System.Data.OleDb.OleDbType]::VarWChar; Value = $usedRange.Item($row, 14).Text.ToString().Trim() },
            @{ Type = [System.Data.OleDb.OleDbType]::VarWChar; Value = $usedRange.Item($row, 15).Text.ToString().Trim() }
        )

        for ($i = 0; $i -lt $values.Count; $i++) {
            $value = $values[$i]
            $parameter = $insert.Parameters.Add("@p$i", $value.Type, 255)
            $parameter.Value = $value.Value
        }

        [void]$insert.ExecuteNonQuery()
    }

    $pk = $connection.CreateCommand()
    $pk.CommandText = "ALTER TABLE [人员信息表] ADD CONSTRAINT [PrimaryKey] PRIMARY KEY ([序号])"
    [void]$pk.ExecuteNonQuery()
} finally {
    if ($workbook) { $workbook.Close($false) }
    if ($excel) { $excel.Quit() }
    Remove-ComObject $usedRange
    Remove-ComObject $worksheet
    Remove-ComObject $workbook
    Remove-ComObject $excel
    if ($connection.State -eq [System.Data.ConnectionState]::Open) {
        $connection.Close()
    }
}

$dao = New-Object -ComObject DAO.DBEngine.120
try {
    $database = $dao.OpenDatabase($OutputAccdb)

    $birthdayField = $database.TableDefs("人员信息表").Fields("出生年月")
    try {
        $birthdayField.Properties("Format") = "yyyy\年mm\月dd\日"
    } catch {
        $property = $birthdayField.CreateProperty("Format", 10, "yyyy\年mm\月dd\日")
        [void]$birthdayField.Properties.Append($property)
    }

    Add-QueryDef -Database $database -Name "人员信息查询表" -Sql @"
SELECT [城市], [区名], [单位], [科室], [姓名], [年龄], [性别], [籍贯], [民族], [出生年月], [身份证号], [学历], [职务], [政治面貌]
FROM [人员信息表]
WHERE [区名] Like Forms![人员信息查询]![地区] & "*"
  AND [单位] Like Forms![人员信息查询]![单位] & "*"
  AND [科室] Like Forms![人员信息查询]![科室] & "*"
  AND [性别] Like Forms![人员信息查询]![性别] & "*"
  AND [民族] Like Forms![人员信息查询]![民族] & "*"
  AND [学历] Like Forms![人员信息查询]![学历] & "*"
  AND [政治面貌] Like Forms![人员信息查询]![政治面貌] & "*"
ORDER BY [序号];
"@
    Add-QueryDef -Database $database -Name "地区表" -Sql "SELECT [区名] FROM [人员信息表] GROUP BY [区名] ORDER BY [区名];"
    Add-QueryDef -Database $database -Name "单位表" -Sql "SELECT [区名], [单位] FROM [人员信息表] GROUP BY [区名], [单位] ORDER BY [区名], [单位];"
    Add-QueryDef -Database $database -Name "科室表" -Sql "SELECT [区名], [单位], [科室] FROM [人员信息表] GROUP BY [区名], [单位], [科室] ORDER BY [区名], [单位], [科室];"
    Add-QueryDef -Database $database -Name "性别表" -Sql "SELECT [性别] FROM [人员信息表] GROUP BY [性别] ORDER BY [性别];"
    Add-QueryDef -Database $database -Name "民族表" -Sql "SELECT [民族] FROM [人员信息表] GROUP BY [民族] ORDER BY [民族];"
    Add-QueryDef -Database $database -Name "学历表" -Sql "SELECT [学历] FROM [人员信息表] GROUP BY [学历] ORDER BY [学历];"
    Add-QueryDef -Database $database -Name "政治面貌表" -Sql "SELECT [政治面貌] FROM [人员信息表] GROUP BY [政治面貌] ORDER BY [政治面貌];"
} finally {
    if ($database) { $database.Close() }
    Remove-ComObject $database
    Remove-ComObject $dao
}

Write-Output "BUILT=$OutputAccdb"
