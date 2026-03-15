@echo off
setlocal

cd /d "%~dp0"

where python > nul 2 > nul
if errorlevel 1 (
    echo [error] Python is not installed or not added to PATH. Please install Python and try again.
    pause
    exit /b 1
)

python "%~dp0autorun.py"

pause