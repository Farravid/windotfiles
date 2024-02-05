winget install Python.Python.3.11
winget install Microsoft.PowerShell

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

python.exe -m pip install --upgrade pip

pip install inquirer
pip install pyuac
pip install pypiwin32

start /b pwsh -Command python %USERPROFILE%\windotfiles\scripts\install.py