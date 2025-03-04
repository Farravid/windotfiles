"""
This script is used to install all the necessary tools and packages for a new development environment.
It uses the Windows Package Manager (winget) and Python's package installer (pip) to install the required software.
It also sets up the necessary configuration files and creates symlinks to the dotfiles repository.

Usage:
1. Navigate to the directory where install.bat is located.
3. Run the batch script as administrator.

Note: This script requires an internet connection and may prompt you to accept EULAs and other agreements.
"""

import os
import subprocess
import logging
import pyuac
from pathlib import Path
import common


def prepare_powershell():
    """
    Installs the latest version of the PSReadLine module and sets the execution policy to RemoteSigned.
    """
    print(f"\n === Installing the last version of module" + common.PURPLE + " PSReadLine " + common.NC + " === \n")
    subprocess.run("pwsh -Command Install-Module PSReadLine -force", shell=True)

def install_pywal():
    """
    Installs the pywal package and its dependencies.
    """
    common.install_pckgs(common.EInstaller.PIP, ["pywal", "colorz", "colorthief", "haishoku"])
    print(f"\n === Importing and running" + common.PURPLE + " winwal " + common.NC + "module to the powershell 7 === \n")
    subprocess.run("pwsh -Command update-winwal " + str(common.WINDOTFILES_ASSETS) + "\\spaceship.jpg", text=True)

def install_wsl():
    print(f"\n === Installing " + common.PURPLE + " Windows Subsystem for Linux (WSL) " + common.NC + "=== \n")
    subprocess.run("pwsh -Command wsl --install", text=True)

def create_sym_links(symlink_file: str, system_path: str = ""):
    """
    Creates a symbolic link to the specified file or folder.

    Args:
        symlink_file (str): The name of the file or folder to create the link to.
        system_path (str, optional): The path of the system folder to create the link in.
    """
    #TODO: This function is not working AS EXPECTED about detecting files

    system_file_path = Path(system_path) if system_path else common.HOME / symlink_file
    dotfiles_file_path = common.WINDOTFILES / symlink_file

    assert dotfiles_file_path.is_file() or dotfiles_file_path.is_dir(), "Trying to symlink an invalid dotfiles file/folder!"

    os.remove(system_file_path)

    if system_file_path.is_file():
        os.remove(system_file_path)
    else:
        path_parent_folder = system_file_path.parent
        if not path_parent_folder.is_dir():
            os.mkdir(path_parent_folder)

    print(f"Symlinking {common.PURPLE + symlink_file + common.NC + ' to ' + common.PURPLE + str(system_file_path) + common.NC}")

    os.symlink(dotfiles_file_path, system_file_path)

def copy_startup_script_to_startup_directory():
    """
    This function copies the 'startup.bat' script to the Windows startup directory.
    The script is located in the same directory as the current script.
    """
    startup_path = '"' + str(common.APPDATA_ROAMING) + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup" + '"'

    common.launch_command("copy startup.bat " + startup_path)


def main():
    """
    The main function of the script.
    """
    input("Pre-installation ready, press enter to continue with the setup. >")

    #common.change_win_color_mode()
    #prepare_powershell()
    #common.launch_command("pwsh -Command Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression", "install for Scoop")    

    #TODO:
    # Use scoop and use export JSON file instead of here
    # Zebar
    # Would be awesome to create a rust gui program to create your own startup stuff
    # Move certain programas to a specifc workspace on startup? Can I do it without the rules?
    # Would be awesome to have a file like variables. something to have general data shared across different stuff like oh my posh theme, shell etc...
    # we need the shortcuts on nushell rather than powershell
    # OneCommander: Colors
    # Investigate settings windows System > For developers
    # Flow launcher: Colors
    # Spicetify (text): setup and colors
    # Discord: colors and themes
    # remove spotify bro and proper install fro spotify
    # Create and show somehow shortcuts for used programms such as Glaze, VSCode, Rider etc....

    # result = subprocess.run('pwsh -Command $PROFILE', shell=True, capture_output=True, text=True)
    # create_sym_links(".config/Microsoft.PowerShell_profile.ps1", result.stdout.strip())
    # create_sym_links(".config/wt/settings.json", str(common.APPDATA_LOCAL) + "\\Packages\\Microsoft.WindowsTerminal_8wekyb3d8bbwe\\LocalState\\settings.json")

    #common.install_pckgs(common.EInstaller.WINGET, common.REQUIRED_WINGET_PROGRAMS)
    
    #create_sym_links(".config/wezterm/wezterm.lua", str(common.HOME) + "\\.config\\wezterm\\wezterm.lua")
    #create_sym_links(".config/wezterm/winwal.toml", str(common.HOME) + "\\.config\\wezterm\\colors\\winwal.toml")
    # create_sym_links(".config/nushell/config.nu", str(common.APPDATA_ROAMING) + "\\nushell\\config.nu")
    # create_sym_links(".config/nushell/env.nu", str(common.APPDATA_ROAMING) + "\\nushell\env.nu")
    #create_sym_links(".config/glazewm/config.yaml", str(common.HOME) + "\\.glzr\\glazewm\\config.yaml")
    #create_sym_links(".config/glazewm/zebar/config.yaml", str(common.HOME) + "\\.glzr\\zebar\\config.yaml")
    #create_sym_links(".config/alacritty.toml", str(common.APPDATA_ROAMING) + "\\alacritty\\alacritty.toml")
    #create_sym_links(".config/fastfetch/config.jsonc")

    # create_sym_links(".config/flameshot.ini", str(common.APPDATA_ROAMING) + "\\flameshot\\flameshot.ini")

    # common.reload_powershell()

    #copy_startup_script_to_startup_directory()
    # # Copying flow_launcher windotfiles settings to the computer installation.
    # common.launch_command("pwsh -Command cp_windotfiles_to_fl") 

    #install_pywal()
    #install_wsl()

    #common.install_optional_pckgs(common.EInstaller.WINGET, common.OPTIONAL_WINGET_PROGRAMS)

    # create_sym_links("vscode/settings.json", str(common.APPDATA_ROAMING) + "\Code\\User\\settings.json")
    # create_sym_links("vscode/keybindings.json", str(common.APPDATA_ROAMING) + "\Code\\User\\keybindings.json")


    # common.install_optional_pckgs(common.EInstaller.CODE, [
    #     "s-nlf-fh.glassit",
    #     "ms-vscode.cpptools",
    #     "ms-vscode.cmake-tools",
    #     "naumovs.color-highlight",
    #     "donjayamanne.python-extension-pack",
    #     "1YiB.rust-bundle",
    #     "dlasagno.wal-theme",
    #     "ms-vscode.powershell",
    #     "eamodio.gitlens",
    #     "wayou.vscode-todo-highlight",
    #     "vscode-icons-team.vscode-icons",
    #     "TabNine.tabnine-vscode",
    #     "yzhang.markdown-all-in-one"], " --force")

    # #TODO: Is this reload necessary?
    # common.reload_powershell()
    # common.launch_command("start glazewm")

    # input("Press enter to close the window. >")


if __name__ == "__main__":
    # if not pyuac.isUserAdmin():
    #     logging.error("You should launch the install.bat script as admin!")
    #     input("Press enter to close the window. >")
    # else:
        main()
