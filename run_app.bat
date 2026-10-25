@echo off
setlocal

rem Always resolve paths relative to this file, not the current terminal folder.
set "PROJECT_DIR=%~dp0matlab1\colour_science_uyen_thy"
set "VENV_DIR=%PROJECT_DIR%\.venv"
set "PYTHON=py"

if not exist "%PROJECT_DIR%\app.py" (
    echo [ERROR] Cannot find the Streamlit app:
    echo         "%PROJECT_DIR%\app.py"
    pause
    exit /b 1
)

%PYTHON% --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found. Install Python 3 from https://www.python.org/
    pause
    exit /b 1
)

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creating a Python virtual environment...
    %PYTHON% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERROR] Could not create the virtual environment.
        pause
        exit /b 1
    )
)

echo Installing or updating dependencies...
"%VENV_DIR%\Scripts\python.exe" -m pip install -r "%PROJECT_DIR%\requirements.txt"
if errorlevel 1 (
    echo [ERROR] Could not install dependencies.
    pause
    exit /b 1
)

echo Starting Streamlit...
cd /d "%PROJECT_DIR%"
"%VENV_DIR%\Scripts\python.exe" -m streamlit run app.py

pause
