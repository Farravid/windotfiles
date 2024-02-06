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

def reload_powershell():
    """
    Reloads the Powershell environment by updating the PATH and reloading the profile.

    Returns:
        None
    """
    launch_command("pwsh -Command $env:Path = [System.Environment]::GetEnvironmentVariable(\"Path\",\"Machine\") + \";\" + [System.Environment]::GetEnvironmentVariable(\"Path\",\"User\")", "a reload for the path")
    launch_command("pwsh -Command Invoke-Expression $PROFILE", "a reloading for the Powershell profile")

def launch_command(command: str, app_name: str = "", show_output: bool = False) -> None:
    """
    Launches an application or a command prompt with the given command.

    Args:
        command (str): The command to be executed.
        app_name (str, optional): The name of the application to be launched.
            Defaults to "".
        show_output (bool, optional): A boolean value indicating whether to show
            the output of the command. Defaults to False.

    Returns:
        None
    """
    if app_name:
        print(f"{PURPLE}== Launching {app_name} =={NC}")

    if show_output:
        subprocess.run(command, shell=True)
    else:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

def change_win_color_mode(to_dark: bool = True) -> None:
    """
    Changes the Windows color mode to dark or light.

    Args:
        to_dark (bool, optional): A boolean value indicating whether to set the
            color mode to dark. If False, the color mode will be set to light.
            Defaults to True.

    Returns:
        None
    """
    theme_value = "0" if to_dark else "1"
    launch_command(
        f"pwsh -Command New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name SystemUsesLightTheme -Value {theme_value} -Type Dword -Force; New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value {theme_value} -Type Dword -Force",
        app_name="a change to the windows color mode",
    )

def launch_glazewm():
    """
    Launches Glazewm, a lightweight and fast window manager for Windows.

    This function first imports the Glazewm color scheme from the
    import_winwal_glaze_colors.py script located in the "colors" folder
    in the Windotfiles repository. It then launches Glazewm using the
    "start" command.

    Returns:
        None
    """
    glaze_colors_script_path = WINDOTFILES_SCRIPTS / "colors/import_winwal_glaze_colors.py"
    launch_command("python " + str(glaze_colors_script_path))
    launch_command("start glazewm")