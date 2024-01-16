@echo off
setlocal

set windotfiles_path=%USERPROFILE%\windotfiles

@rem Run WM
%windotfiles_path%\GlazeWM\GlazeWM_x64_2.1.0.exe

rem Set the path to your Python script
set python_script_path=python %windotfiles_path%\scripts\setup_selector.py

rem Launch PowerShell and execute the Python script
powershell -Command "& {%python_script_path%}"

endlocal