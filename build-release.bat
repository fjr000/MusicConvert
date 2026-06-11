@echo off
REM 一键打包便携版 release(双击运行)。
REM 优先 PowerShell 7 (pwsh),回退 Windows PowerShell。
setlocal
set "SCRIPT=%~dp0scripts\build-release.ps1"
where pwsh >nul 2>nul
if %errorlevel%==0 (
    pwsh -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%" %*
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%" %*
)
echo.
pause
