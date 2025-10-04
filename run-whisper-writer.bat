@echo off
setlocal

REM Resolve directory of this script so it works when double-clicked
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%" >nul

REM Launch the app through pythonw so the console window can close immediately
start "" "%SCRIPT_DIR%venv\Scripts\pythonw.exe" "%SCRIPT_DIR%run.py"

popd >nul
endlocal
