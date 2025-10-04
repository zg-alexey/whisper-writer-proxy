@echo off
setlocal

REM Resolve directory of this script so it works when double-clicked
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%" >nul

REM Activate the virtual environment and launch the app
call venv\Scripts\activate.bat
python run.py

REM Keep the window open if the app exits immediately
if errorlevel 1 pause

popd >nul
endlocal
