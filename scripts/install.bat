@REM Installs Python 3.11 and PowerShell from the Microsoft Store, adds Python to the PATH, and upgrades pip
@REM Installs the inquirer, pyuac, and pypiwin32 libraries using pip
@REM Runs the install.py script in the user's windotfiles\scripts directory in PowerShell as a background process

pwsh -Command Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
pwsh -Command Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

@rem install scoop and all the stuff
scoop install python
winget install Microsoft.PowerShell


@rem add buckets for scoop
@rem exe the registry for scoop for allowing other programs to see python

pwsh -Command $env:Path = [System.Environment]::GetEnvironmentVariable(\"Path\",\"Machine\") + \";\" + [System.Environment]::GetEnvironmentVariable(\"Path\",\"User\")

python -m pip install --upgrade pip

pip install inquirer pyuac pypiwin32

start /b pwsh -Command python %USERPROFILE%\windotfiles\scripts\install.py 