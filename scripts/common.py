import subprocess
import os
from pathlib import Path

#########################################
# TERMINAL COLORS
#########################################
PURPLE = '\033[0;35m'
NC = '\033[0m'

#########################################
# PATHS
#########################################
HOME : Path = Path.home()
WINDOTFILES : Path = Path.home() / "windotfiles/"
WINDOTFILES_SCRIPTS : Path = Path.home() / "windotfiles/scripts/"
WINDOTFILES_ASSETS : Path = Path.home() / "windotfiles/assets/"
APPDATA_ROAMING : Path = os.environ['appdata']
APPDATA_LOCAL : Path = os.environ['LocalAppData']

#########################################
# FUNCTIONS
#########################################

## Reloads the Powershell's profile
##
def reload_profile():
    launch_command("pwsh --Command Invoke-Expression $PROFILE", "a reloading for the Powershell profile")

## Simply launch a terminal command with an optional debugging
##
def launch_command(command, app_name = "", show_output = False):
    if app_name != "":
        print(f"{PURPLE} == Launching {app_name} == {NC}")
    
    if show_output: subprocess.run(command, shell=True)
    else: subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

## Launch the tiling windows manager GlazeWM
## It also import the colors to the GlazeWM config file from winwal
## 
def launch_glazewm():
    glaze_colors_script_path = WINDOTFILES_SCRIPTS / "colors/import_winwal_glaze_colors.py"
    launch_command("python " + str(glaze_colors_script_path))
    launch_command("start glazewm")