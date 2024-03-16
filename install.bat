@echo off

REM Define Python installer URL
set "pythonZipUrl=https://www.python.org/ftp/python/3.10.2/python-3.10.2-embed-amd64.zip"

REM Define temporary directory to extract Python
set "pythonTempDir=%TEMP%\python"

REM Download Python embeddable package
powershell -Command "Invoke-WebRequest -Uri '%pythonZipUrl%' -OutFile '%pythonTempDir%\python.zip'"

REM Unzip Python embeddable package
powershell -Command "Expand-Archive -Path '%pythonTempDir%\python.zip' -DestinationPath '%pythonTempDir%'"

REM Set Python directory
set "pythonDir=%pythonTempDir%\Python310"

REM Add Python to PATH
set "PATH=%pythonDir%;%PATH%"

REM Install pip
python -m ensurepip

REM Verify Python and pip installation
python --version
pip --version

REM Install dependencies from requirements.txt
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found. Skipping dependency installation.
)

REM Create directory
mkdir "static"

echo All actions completed.
pause
