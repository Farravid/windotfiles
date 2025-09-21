@REM Installs Python 3.11 and PowerShell from the Microsoft Store, adds Python to the PATH, and upgrades pip
@REM Installs the inquirer, pyuac, and pypiwin32 libraries using pip
@REM Runs the install.py script in the user's windotfiles\scripts directory in PowerShell as a background process

pwsh -Command Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

python -m pip install --upgrade pip
pip install inquirer pyuac pypiwin32

start /b pwsh -Command python %USERPROFILE%\windotfiles\scripts\install.py 