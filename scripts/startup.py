"""
This script is used to display different programs depending on the work.

It uses the inquirer library to prompt the user for a choice, and then uses a 
match statement to determine which setup to display. If the user chooses to 
launch default apps with the setup, the launch_default_apps function is called.

The display_decorator function uses the neofetch command to display system 
information, and then prints a decorative banner.

The common module contains functions that are used to launch applications and 
run commands.

This script uses Python 3.11 features, such as the match statement and the 
willingness to use non-ASCII characters in strings.
"""

import time
import inquirer
import os
import glob
import common
import subprocess
from pathlib import Path

PURPLE = '\033[0;35m'
NC = '\033[0m'


def display_decorator():
    """
    This function uses the neofetch command to display system information, and 
    then prints a decorative banner.
    """
    subprocess.Popen("neofetch", shell=True)
    time.sleep(0.5)
    print(f"{PURPLE}" * 60 + NC)
    print("== Default apps ==")
    print("[WS1] Google Chrome")
    print("[WS3] Spotify, Discord")
    print(f"{PURPLE}" * 60 + NC)


def launch_default_apps():
    """
    This function launches the default apps for each workspace.
    """
    common.launch_command("start /b chrome.exe", "Google Chrome")
    common.launch_command("start /b " + str(common.APPDATA_ROAMING / Path("Spotify/Spotify.exe")), "Spotify")

    discord_folder = next((d for d in glob.glob(os.path.join(str(common.APPDATA_LOCAL / Path("Discord")), 'app*')) if os.path.isdir(d)), None)
    common.launch_command("start /b " + str(Path(discord_folder + "/Discord.exe")), "Discord")


def launch_c_setup():
    """
    This function is not implemented yet.
    """
    pass

def launch_frg_setup():
    """
    This function launches the setup for working. Slack, Perforce, Unreal...
    """
    common.launch_command(str(common.PROGRAM_FILES) + "\\Slack\\Slack.exe", "Slack", False, True)
    common.launch_command(str(common.PROGRAM_FILES) + "\\Perforce\\p4v.exe", "Perforce", False, True)
    common.launch_command(str(common.PROGRAM_FILES) + "\\JetBrains\JetBrains Rider 2023.3.3\\bin\\rider64.exe", "Rider", False, True)
    

def launch_godot_setup():
    """
    This function launches the Godot game engine and the GitHub Desktop app.
    """
    common.launch_command("pwsh -Command godot", "Godot (Suipe)")
    common.launch_command("start /b " + str(common.APPDATA_LOCAL / Path("GitHubDesktop/GitHubDesktop.exe")), "Github Desktop")


def main():
    """
    This function is the main entry point of the script. It uses the inquirer 
    library to prompt the user for a choice, and then calls the appropriate 
    function based on the choice.
    """
    options = [
        inquirer.List('choice',
                      message="Select a setup to display:",
                      choices = ["FRG", "C++", "Godot", "None"],

                      )
    ]

    answer = inquirer.prompt(options)
    show_default_apps = inquirer.confirm("Do you want to launch default apps with this setup?", default=True)

    if show_default_apps:
        launch_default_apps()

    match answer['choice']:
        case 'C++'  : launch_c_setup()
        case 'Godot': launch_godot_setup()
        case 'FRG': launch_frg_setup()

if __name__ == "__main__":
    common.launch_glazewm()
    display_decorator()
    main()