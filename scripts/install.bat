@REM Installs Python 3.11 and PowerShell from the Microsoft Store, adds Python to the PATH, and upgrades pip
@REM Installs the inquirer, pyuac, and pypiwin32 libraries using pip
@REM Runs the install.py script in the user's windotfiles\scripts directory in PowerShell as a background process

winget install Python.Python.3.11
winget install Microsoft.PowerShell

pwsh -Command $env:Path = [System.Environment]::GetEnvironmentVariable(\"Path\",\"Machine\") + \";\" + [System.Environment]::GetEnvironmentVariable(\"Path\",\"User\")

python.exe -m pip install --upgrade pip

pip install inquirer pyuac pypiwin32

start /b pwsh -Command python .\scripts\install.py