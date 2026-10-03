@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo First run: creating the local Python environment...
  py -3 -m venv .venv
  if errorlevel 1 goto failed
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 goto failed
)
".venv\Scripts\python.exe" scripts\setup_cartridge_support.py
if errorlevel 1 echo Optional cartridge support setup failed. Other modes remain available; rerun Setup cartridge support.cmd later.
".venv\Scripts\python.exe" run.py %*
if errorlevel 1 goto failed
exit /b 0
:failed
echo.
echo Startup failed. Install Python 3.12 or newer, then try again.
echo If dependencies are missing, run .venv\Scripts\python.exe -m pip install -r requirements.txt
pause
exit /b 1
