import subprocess
import sys
import os
import winreg
import inquirer
from pathlib import Path

if Path(__file__).resolve().parent.parent != Path.home() / "windotfiles":
    print("ERROR: windotfiles must live at %USERPROFILE%\\windotfiles", file=sys.stderr)
    sys.exit(1)

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
APPDATA_ROAMING : Path = Path(os.environ['appdata'])
APPDATA_LOCAL : Path = Path(os.environ['LocalAppData'])
PROGRAM_FILES : Path = Path(os.environ['programfiles'])

#########################################
# INSTALLED ARTIFACTS (shared by install.py / uninstall.py)
#########################################
ZEBAR_WIDGET = "mushfikurr.overline-zebar@1.0.0"

# (repo file, symlink destination) pairs.
SYMLINKS = [
    (".config/wezterm/wezterm.lua",         HOME / ".config/wezterm/wezterm.lua"),
    (".config/wezterm/winwal.toml",         HOME / ".config/wezterm/colors/winwal.toml"),
    (".config/glazewm/config.yaml",         HOME / ".glzr/glazewm/config.yaml"),
    (".config/glazewm/zebar/settings.json", HOME / ".glzr/zebar/settings.json"),
    (".config/nushell/config.nu",           APPDATA_ROAMING / "nushell/config.nu"),
    (".config/flowlauncher/Settings.json",  APPDATA_ROAMING / "FlowLauncher/Settings/Settings.json"),
    (".config/flameshot.ini",               APPDATA_ROAMING / "flameshot/flameshot.ini"),
    (".config/fastfetch/config.jsonc",      HOME / ".config/fastfetch/config.jsonc"),
    (".config/yazi/keymap.toml",            APPDATA_ROAMING / "yazi/config/keymap.toml"),
    (".config/yazi/yazi.toml",              APPDATA_ROAMING / "yazi/config/yazi.toml"),
    (".config/opencode/opencode.jsonc",     HOME / ".config/opencode/opencode.jsonc"),
    (".config/opencode/package.json",       HOME / ".config/opencode/package.json"),
    (".config/opencode/package-lock.json",  HOME / ".config/opencode/package-lock.json"),
]

PIP_PACKAGES = ["pywal", "colorz", "colorthief", "haishoku"]

#########################################
# PROGRAMS
#########################################
REQUIRED_WINGET_PROGRAMS = [
        "wez.wezterm.nightly",
        "nushell",
        "glazewm",
        "glzr-io.zebar",
        "Git.Git",
        "Github.GitLFS",
        "GitHub.CLI",
        "DEVCOM.JetBrainsMonoNerdFont",
        "Flow-Launcher.Flow-Launcher",
        "voidtools.Everything",
        "JanDeDobbeleer.OhMyPosh",
        "fastfetch",
        "sxyazi.yazi",
        "Neovim.Neovim",
        "oschwartz10612.Poppler",
        "junegunn.fzf",
        "sharkdp.fd",
        "ImageMagick.ImageMagick",
        "flameshot",
        "SST.opencode"]

OPTIONAL_WINGET_PROGRAMS = [
        "JetBrains.Rider",
        "ProtonVPN",
        "Spotify.Spotify",
        "Brave.Brave",
        "GitHub.GitHubDesktop",
        "Discord.Discord",
        "Ollama.Ollama",
        "OBSProject.OBSProject",
        "Microsoft.DirectX",
        "Nvidia.GeForceExperience",
        "Stoat.Stoat"]

#########################################
# TYPES
#########################################
class EInstaller():
    """
    Enum class for providing an easier way to select the installer of a package/library/extension
    """
    WINGET = "winget install --accept-source-agreements --accept-package-agreements "
    WINGET_UPGRADE = "winget upgrade "
    PIP = "pip install "

#########################################
# FUNCTIONS
#########################################

def reload_powershell():
    """
    Refreshes this process's PATH from the registry so newly-installed
    programs are visible to later subprocess calls.

    Returns:
        None
    """
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
        machine_path = winreg.QueryValueEx(key, "Path")[0]
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
        user_path = winreg.QueryValueEx(key, "Path")[0]
    os.environ["Path"] = os.path.expandvars(machine_path + ";" + user_path)

def launch_command(command: str, app_name: str = "", show_output: bool = False, use_popen : bool = False, detached: bool = False) -> None:
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

    if detached:
        # ponytail: WezTerm runs its shell in a kill-on-close job object, so
        # anything we launch dies when the terminal window closes. Break the new
        # process out of that job so setup apps outlive the terminal.
        flags = (subprocess.CREATE_BREAKAWAY_FROM_JOB
                 | subprocess.DETACHED_PROCESS
                 | subprocess.CREATE_NEW_PROCESS_GROUP)
        try:
            subprocess.Popen(command, shell=True, creationflags=flags,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            # Job forbids breakaway; fall back to a normal detached spawn.
            subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL)
        return

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
        f"pwsh -NoProfile -Command New-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name SystemUsesLightTheme -Value {theme_value} -Type Dword -Force; New-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value {theme_value} -Type Dword -Force",
        app_name="a change to the windows color mode",
    )