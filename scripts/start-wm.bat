@echo off
setlocal

rem Set the path to your Python script
set python_script_path=python %USERPROFILE%\windotfiles\scripts\setup_selector.py

rem Launch PowerShell and execute the Python script
powershell.exe -Command "& {%python_script_path%}"

endlocal