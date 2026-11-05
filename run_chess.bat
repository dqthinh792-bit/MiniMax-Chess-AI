@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -m pip install -r requirements.txt
  py -3 main.py
) else (
  python -m pip install -r requirements.txt
  python main.py
)
if errorlevel 1 (
  echo.
  echo Chess AI could not start. Read the error above.
  pause
)
