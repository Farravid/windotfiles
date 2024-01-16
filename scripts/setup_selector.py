# Setup selector for displaying different programs depending on the work

import subprocess
import time
import inquirer

Purple = '\033[0;35m'
NC = '\033[0m'

def display_decorator():
    #subprocess.Popen("neofetch --config ~/dotfiles/.config/neofetch/small_config.conf", shell=True)
    time.sleep(0.5)
    print("")
    print("== Default apps ==")
    print("[WS1] Terminal")
    print("[WS2] Google Chrome")
    print("[WS3] Spotify, Discord, Cava")
    print("")


def launch_app(command, app_name, time_to_sleep = 0.0, workspace = ""):
    print(f"{Purple} == Launching {app_name} == {NC}")
    subprocess.Popen(command, shell=True, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    #time.sleep(time_to_sleep)

    #if(workspace):
    #   subprocess.Popen(f"i3-msg 'move container to workspace {workspace}'", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def launch_default_apps():
    #launch_app("kitty", "Blank Kitty")
    launch_app("C:/Program Files/Google/Chrome/Application/chrome.exe", "Google Chrome", 2, "2:Notes")
    #launch_app("spotify", "Spotify", 2, "3:Media")
    #launch_app("discord", "Discord", 5, "3:Media")
    #launch_app("kitty --hold -e cava", "Cava", 1, "3:Media")

def launch_c_setup():
    print("Performing Action 1")
    # Add your logic for Action 1 here

def launch_godot_setup():
    launch_app("cd ~/Documents/GitHub/ProjectoAmador && scripts/linux/launch_godot_editor.sh", "Godot", 1)
    launch_app("github-desktop", "Github Desktop", 1, "2:Notes")

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
    main()