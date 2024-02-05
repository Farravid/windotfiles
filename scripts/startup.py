# Setup selector for displaying different programs depending on the work

import time
import inquirer
import os
import glob
import common
import subprocess
from pathlib import Path

Purple = '\033[0;35m'
NC = '\033[0m'

def display_decorator():
    subprocess.Popen("neofetch", shell=True)
    time.sleep(0.5)
    print("")
    print("== Default apps ==")
    print("[WS1] Terminal")
    print("[WS2] Google Chrome")
    print("[WS3] Spotify, Discord")
    print("")

def launch_default_apps():
    common.launch_command("start /b chrome.exe", "Google Chrome")
    common.launch_command("start /b wt", "Windows Terminal")
    common.launch_command("start /b spotify", "Spotify")

    discord_folder = next((d for d in glob.glob(os.path.join(str(common.APPDATA_LOCAL / Path("Discord")), 'app*')) if os.path.isdir(d)), None)
    common.launch_command("start /b " + str(Path(discord_folder + "/Discord.exe")), "Discord")

def launch_c_setup():
    pass

def launch_godot_setup():
    common.launch_command("pwsh -Command godot", "Godot (Suipe)")
    common.launch_command("start /b " + str(common.APPDATA_LOCAL / Path("GitHubDesktop/GitHubDesktop.exe")), "Github Desktop")

def main():
    options = [
        inquirer.List('choice',
                      message="Select a setup to display:",
                      choices = ["C++", "Godot", "None"],

                      )
    ]

    answer = inquirer.prompt(options)
    show_default_apps = inquirer.confirm("Do you want to launch default apps with this setup?", default=True)

    if(show_default_apps): launch_default_apps()

    match answer['choice']:
        case 'C++'  : launch_c_setup()
        case 'Godot': launch_godot_setup()

if __name__ == "__main__":
    common.launch_glazewm()
    display_decorator()
    main()