@echo off

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python 3.10. Please wait...
    REM Download Python installer
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe', '%TEMP%\python_installer.exe')"
    REM Install Python silently
    %TEMP%\python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    REM Wait for Python installation to complete
    timeout /t 10 /nobreak >nul
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed. Installing pip. Please wait...
    REM Install pip
    python -m ensurepip
)

REM Verify Python and pip installation
python --version
pip --version

REM Install dependencies from requirements.txt
if exist requirements.txt (
    python -m pip install -r requirements.txt
) else (
    echo requirements.txt not found. Skipping dependency installation.
)

REM Create directory
mkdir "static"

echo All actions completed.
REM Close the command prompt window after 3 seconds
ping 127.0.0.1 -n 3 > nul
exit
