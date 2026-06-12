@echo off
setlocal
set "SCRIPT=%~dp0scripts\build-release.ps1"

REM Try to find Python
set PYTHON_CMD=
where python >nul 2>nul
if %errorlevel% equ 0 set PYTHON_CMD=python

if "%PYTHON_CMD%"=="" (
    where python3 >nul 2>nul
    if %errorlevel% equ 0 set PYTHON_CMD=python3
)

if "%PYTHON_CMD%"=="" (
    echo ERROR: Python not found in PATH
    echo Please ensure Python is installed and added to PATH
    echo Or activate your conda/venv environment first
    pause
    exit /b 1
)

REM Use PowerShell to run build script with detected Python
where pwsh >nul 2>nul
if %errorlevel%==0 (
    pwsh -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%" -Python %PYTHON_CMD%
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%" -Python %PYTHON_CMD%
)
echo.
pause
