import subprocess
import os
import inquirer
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
PROGRAM_FILES : Path = Path(os.environ['programfiles'])

#########################################
# PROGRAMS
#########################################
REQUIRED_WINGET_PROGRAMS = [
        "glzr-io.glazewm",
        "Git.Git",
        "Github.GitLFS",
        "DEVCOM.JetBrainsMonoNerdFont -v \"2.3.3\" -e",
        "Microsoft.WindowsTerminal",
        "Flow-Launcher.Flow-Launcher",
        "Microsoft.NuGet",
        "JanDeDobbeleer.OhMyPosh",
        "neofetch"]

OPTIONAL_WINGET_PROGRAMS = [
        "Clement.bottom",
        "DygmaLabs.Bazecor",
        "Spotify.Spotify",
        "Spicetify.Spicetify",
        "Google.Chrome",
        "GitHub.GitHubDesktop",
        "Discord.Discord",
        "Obsidian.Obsidian",
        "Neovim.Neovim",
        "OBSProject.OBSProject",
        "Microsoft.DirectX",
        "Nvidia.GeForceExperience",
        "voidtools.Everything",
        "Microsoft.VisualStudioCode",
        "Microsoft.VisualStudio.2022.BuildTools",
        "Microsoft.VisualStudio.2022.Community",
        "Rustlang.Rustup"]

#########################################
# TYPES
#########################################
class EInstaller():
    """
    Enum class for providing an easier way to select the installer of a package/library/extension
    """
    WINGET = "winget install --accept-source-agreements --accept-package-agreements "
    WINGET_UPDGRADE = "winget upgrade "
    PIP = "pip install "
    CODE = "code --install-extension "

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

def launch_command(command: str, app_name: str = "", show_output: bool = False, use_popen : bool = False) -> None:
    """
    Launches an application or a command prompt with the given command.

    Args:
        command (str): The command to be executed.
        app_name (str, optional): The name of the application to be launched.
            Defaults to "".
        show_output (bool, optional): A boolean value indicating whether to show
            the output of the command. Defaults to False.
        use_popen (bool, optional): A boolean value indicating whether to run
            the command or using subprocess.pOpen to run the command. Defaults to False.

    Returns:
        None
    """
    if app_name:
        print(f"{PURPLE}== Launching {app_name} =={NC}")

    if show_output:
        if use_popen: subprocess.Popen(command, shell=True)
        else: subprocess.run(command, shell=True)
    else:
        if use_popen: subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL)
        else: subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

def install_pckgs(installer: EInstaller, pkg_names: list, commands: str = ""):
    """
    Installs the specified packages using the specified installer.

    Args:
        installer (EInstaller): The installer to use (winget, pip, or code).
        pkg_names (list): The names of the packages to install.
        commands (str, optional): Additional commands to pass to the installer.
    """
    for pkg_name in pkg_names:
        print(f"\n === Installing " + PURPLE + pkg_name + NC + " with " + installer + " === \n")
        launch_command(installer + pkg_name + commands, "", True)


def install_optional_pckgs(installer: EInstaller, pkg_names: list, commands: str = ""):
    """
    Installs or uninstalls the specified optional packages using the specified installer.

    Args:
        installer (EInstaller): The installer to use (winget, pip, or code).
        pkg_names (list): The names of the packages to install or uninstall.
        commands (str, optional): Additional commands to pass to the installer.
    """
    for pkg_name in pkg_names:

        message = f'Do you want to {"" if installer == EInstaller.PIP else "in"}stall ' + PURPLE + pkg_name + NC + ' ?'
        question = [
            inquirer.List(
                "choice", message, ["Yes", "No"],
            ),
        ]

        answer = inquirer.prompt(question)

        if answer["choice"] == "Yes":
            install_pckgs(installer, [pkg_name], commands)

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