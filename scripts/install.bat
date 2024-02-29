@REM Installs Python 3.11 and PowerShell from the Microsoft Store, adds Python to the PATH, and upgrades pip
@REM Installs the inquirer, pyuac, and pypiwin32 libraries using pip
@REM Runs the install.py script in the user's windotfiles\scripts directory in PowerShell as a background process

@REM winget install --accept-source-agreements --accept-package-agreements Python.Python.3.11
@REM winget install Microsoft.PowerShell

@REM pwsh -Command $env:Path = [System.Environment]::GetEnvironmentVariable(\"Path\",\"Machine\") + \";\" + [System.Environment]::GetEnvironmentVariable(\"Path\",\"User\")

@REM python.exe -m pip install --upgrade pip

pip install inquirer pyuac pypiwin32

::start /b pwsh -Command python .\scripts\install_ci.py
pwsh -Command python .\scripts\install_ci.py
