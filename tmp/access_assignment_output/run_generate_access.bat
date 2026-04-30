@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ================================================
echo Access assignment generator
echo This BAT is ASCII encoded to avoid CMD mojibake.
echo ================================================
echo.

if not exist "create_access_assignment.vbs" (
  echo ERROR: create_access_assignment.vbs not found in current folder.
  pause
  exit /b 1
)

if not exist "source.xls" (
  echo ERROR: source.xls not found in current folder.
  echo Please keep source.xls in the same folder as this BAT.
  pause
  exit /b 1
)

cscript //nologo "%~dp0create_access_assignment.vbs"
set "ERR=%ERRORLEVEL%"

echo.
if "%ERR%"=="0" (
  echo DONE. Please check the generated ACCDB file in this folder.
) else (
  echo FAILED. ErrorLevel=%ERR%
  echo If Access opened a warning, close Access and run again after enabling trusted VBA project access.
)

echo.
pause
exit /b %ERR%
