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
import json
import subprocess
from pathlib import Path
import ctypes

PURPLE = '\033[0;35m'
NC = '\033[0m'

def get_window_id(process_name: str):
    """
    This function retrieves the window ID of a specific process running on the system.
    It uses the 'glazewm query windows' command to obtain a list of all running windows,
    then iterates through the list to find the window with the matching process name.

    Parameters:
    process_name (str): The name of the process for which to retrieve the window ID.

    Returns:
    int | None: The window ID of the specified process, or None if no matching process is found.
    """
    try:
        result = subprocess.run(["glazewm", "query", "windows"], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        windows = data.get("data", {}).get("windows", [])

        for window in windows:
            if window.get("processName") == process_name:
                return window.get("id")

        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def move_window_to_workspace(process_name, workspace):
    """
    Move a window associated with a specific process to a designated workspace.

    This function attempts to move a window identified by its process name to a specified
    workspace using the glazewm window manager. It first retrieves the window ID for the
    given process name and then uses glazewm commands to move the window.

    Parameters:
    process_name (str): The name of the process whose window should be moved.
    workspace (int): The number of the workspace to which the window should be moved.
    """

    window_id = get_window_id(process_name)
    try:
        subprocess.run(["glazewm", "command", "--id", window_id, "move", "--workspace", str(workspace)], check=True)
        print(f"Moved window {window_id} to workspace {workspace}")
    except Exception as e:
        print(f"Error moving window: {e}")

def display_decorator():
    """
    This function uses the neofetch command to display system information, and 
    then prints a decorative banner.
    """
    subprocess.Popen("fastfetch", shell=True)
    time.sleep(1.5)
    print(f"{PURPLE}" * 60 + NC)
    print("== Default apps ==")
    print("[WS2] Google Chrome")
    print("[WS3] Spotify, Discord")
    print(f"{PURPLE}" * 60 + NC)

def launch_default_apps():
    """
    This function launches the default apps for each workspace.
    """
    #common.launch_command("glazewm command move --workspace 1")
    common.launch_command("start /b chrome.exe", "Google Chrome")
    common.launch_command("start /b " + str(common.APPDATA_ROAMING / Path("Spotify/Spotify.exe")), "Spotify")

    discord_folder = next((d for d in glob.glob(os.path.join(str(common.APPDATA_LOCAL / Path("Discord")), 'app*')) if os.path.isdir(d)), None)
    common.launch_command("start /b " + str(Path(discord_folder + "/Discord.exe")), "Discord")


def launch_windotfiles_setup():
    """
    This function launches the VSCode with windotfiles, a terminal and the GitHub Desktop app.
    """
    common.launch_command("start /b wezterm-gui", "Windows Terminal")
    common.launch_command("pwsh -Command cwindotfiles", "Windotfiles in VSCode")
    common.launch_command("start /b " + str(common.APPDATA_LOCAL / Path("GitHubDesktop/GitHubDesktop.exe")), "Github Desktop")

def launch_frg_setup():
    """
    This function launches the setup for working. Slack, Perforce, Unreal...
    """
    common.launch_command(str(common.PROGRAM_FILES) + "\\Slack\\Slack.exe", "Slack", False, True)
    common.launch_command(str(common.PROGRAM_FILES) + "\\Perforce\\p4v.exe", "Perforce", False, True)
    common.launch_command(str(common.PROGRAM_FILES) + "\\JetBrains\\JetBrains Rider 2023.3.3\\bin\\rider64.exe", "Rider", False, True)
    

def launch_godot_setup():
    """
    This function launches the Godot game engine and the GitHub Desktop app.
    """
    common.launch_command("pwsh -Command godot", "Godot (Suipe)")
    common.launch_command("start /b " + str(common.APPDATA_LOCAL / Path("GitHubDesktop/GitHubDesktop.exe")), "Github Desktop")

def move_windows_to_workspaces():
    move_window_to_workspace("wezterm-gui", 1)
    move_window_to_workspace("Godot_v4", 1)
    move_window_to_workspace("rider64", 1)
    move_window_to_workspace("Code", 1)
    move_window_to_workspace("p4v", 2)
    move_window_to_workspace("GitHubDesktop", 2)
    move_window_to_workspace("chrome", 2)
    move_window_to_workspace("Slack", 2)
    move_window_to_workspace("Spotify", 3)
    move_window_to_workspace("Discord", 3)
    move_window_to_workspace("ProtonVPN", 4)


def main():
    """
    This function is the main entry point of the script. It uses the inquirer 
    library to prompt the user for a choice, and then calls the appropriate 
    function based on the choice.
    """
   
    ctypes.windll.kernel32.SetConsoleTitleW("Startup")

    options = [
        inquirer.List('choice',
                      message="Select a setup to display:",
                      choices = ["FRG", "Suipe", "Windotfiles", "None"],

                      )
    ]

    answer = inquirer.prompt(options)
    show_default_apps = inquirer.confirm("Do you want to launch default apps with this setup?", default=True)

    common.launch_command(str(common.WINDOTFILES / Path(".config/glazewm/zebar/start.bat")), " Zebar")
    ## Test if no windows is necessary for the above command
    #subprocess.Popen(["zebar", "open", "bar"], creationflags=subprocess.CREATE_NO_WINDOW)

    if show_default_apps:
        launch_default_apps()

    match answer['choice']:
        case 'Windotfiles'  : launch_windotfiles_setup()
        case 'Suipe'        : launch_godot_setup()
        case 'FRG'          : launch_frg_setup()
    
    time.sleep(1)
    move_windows_to_workspaces()

if __name__ == "__main__":
    common.launch_command("start glazewm")
    common.launch_command("start /b " + str(common.WINDOTFILES / Path("vendor/buttery-taskbar2/buttery-taskbar.exe")))
    common.launch_command("glazewm command set-floating && glazewm command size --width 900 --height 900")
    display_decorator()
    main()

