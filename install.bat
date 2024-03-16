@echo off

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Python...
    
    REM Define Python installer URL
    set "pythonInstallerUrl=https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe"

    REM Define Python installer file path
    set "pythonInstallerPath=%TEMP%\python-installer.exe"

    REM Download Python installer
    echo Downloading Python installer...
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%pythonInstallerUrl%', '%pythonInstallerPath%')"

    REM Install Python silently
    echo Installing Python silently...
    "%pythonInstallerPath%" /quiet InstallAllUsers=1 PrependPath=1

    REM Verify Python installation
    echo Verifying Python installation...
    python --version

    REM Clean up Python installer
    echo Cleaning up Python installer...
    del "%pythonInstallerPath%"
) else (
    echo Python is already installed.
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing or upgrading pip...
    
    REM Install or upgrade pip
    python -m pip install --upgrade pip

    REM Verify pip installation
    echo Verifying pip installation...
    pip --version
) else (
    echo pip is already installed.
)

REM Check if requirements.txt exists
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    python -m pip install -r requirements.txt
) else (
    echo requirements.txt not found. Skipping dependency installation.
)

REM Create directory
echo Creating directory "static"...
mkdir "static"

echo All actions completed.
pause
