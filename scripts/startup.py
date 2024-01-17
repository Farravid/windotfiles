# Setup selector for displaying different programs depending on the work

import subprocess
import time
import inquirer
from pathlib import Path

Purple = '\033[0;35m'
NC = '\033[0m'

def display_decorator():
    subprocess.Popen("neofetch --config ~/dotfiles/.config/neofetch/small_config.conf", shell=True)
    time.sleep(0.5)
    print("")
    print("== Default apps ==")
    print("[WS1] Terminal")
    print("[WS2] Google Chrome")
    print("[WS3] Spotify, Discord, Cava")
    print("")


def launch_app(command, app_name, time_to_sleep = 0.0, workspace = ""):
    print(f"{Purple} == Launching {app_name} == {NC}")
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    #time.sleep(time_to_sleep)

    #if(workspace):
    #   subprocess.Popen(f"i3-msg 'move container to workspace {workspace}'", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def launch_default_apps():
    launch_app("start /b chrome.exe", "Google Chrome", 2, "2:Notes")

def launch_c_setup():
    pass

def launch_godot_setup():
    pass

def main():
    options = [
        inquirer.List('choice',
                      message="Select a setup to display:",
                      choices = ["C++", "Godot", "None"]
                      )
    ]

    answer = inquirer.prompt(options)
    show_default_apps = inquirer.confirm("Do you want to launch default apps with this setup?", default=True)

    if(show_default_apps): launch_default_apps()

    match answer['choice']:
        case 'C++'  : launch_c_setup()
        case 'Godot': launch_godot_setup()

if __name__ == "__main__":
    display_decorator()
    glaze_colors_script_path = Path.home() / "windotfiles/scripts/import_winwal_glaze_colors.py"
    launch_app("python " + str(glaze_colors_script_path), "script for reloading colors for GlazeWM from winwal")
    launch_app("start glazewm", "Glaze (Tilling Windows Manager)")
    main()