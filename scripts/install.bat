@REM Upgrades pip, installs the Python libraries the scripts need (see requirements.txt),
@REM then runs install.py in the user's windotfiles\scripts directory as a background process.

pwsh -Command Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

python -m pip install --upgrade pip
pip install -r "%USERPROFILE%\windotfiles\scripts\requirements.txt"

start /b pwsh -Command python %USERPROFILE%\windotfiles\scripts\install.py 