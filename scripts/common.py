import subprocess
import os
import sys
import time
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
    launch_command("python " + str(glaze_colors_script_path), "a reload for GlazeWM color scheme")
    launch_command("start glazewm")

# TODO: We may have to check if the user has rust installed

##
##
def update_dygma_winwal():
    dygma_colors_script_path = WINDOTFILES_SCRIPTS / "colors/import_winwal_dygma_colors.py"
    launch_command("python " + str(dygma_colors_script_path), "a reload for dygma color scheme")
    launch_command("pwsh -Command cargo run --manifest-path $env:USERPROFILE\windotfiles\dygma\dygma_api\Cargo.toml --release", "rust script for applying colors to dygma")

##
##
def update_winwal():
    launch_command("pwsh -Command Update-WalTheme -Image " + os.path.abspath(sys.argv[1]), "Update-WalTheme to update color schemes with the given wallpaper")
    update_dygma_winwal()
    launch_command("pwsh -Command Stop-Process -Name GlazeWM -Force", "a reload for GlazeWM")
    launch_glazewm()
    launch_command("pwsh -Command Stop-Process -Name WindowsTerminal -Force")
    subprocess.Popen("start /b wt", shell=True)

# TODO: Maybe create another script because this doesnt make any sense
def main():
    update_winwal()

if __name__ == "__main__":
    main()