@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" scripts\setup_cartridge_support.py
) else (
  py -3 scripts\setup_cartridge_support.py
)
if errorlevel 1 pause
