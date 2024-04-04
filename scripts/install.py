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
    print(f"\n === Setting the execution policy for powershell scripts for this user to " + common.PURPLE + " RemoteSigned " + common.NC + " === \n")
    subprocess.run("pwsh -Command Set-ExecutionPolicy RemoteSigned -Scope CurrentUser", shell=True, text=True)
    print("\n === Importing the " + common.PURPLE + " start-dotfiles.xml " + common.NC + " task to the Task Scheduler === \n")
    subprocess.run(["pwsh", "-Command", f"Register-ScheduledTask -Xml (Get-Content '{common.WINDOTFILES}\\tasks\\start-dotfiles.xml' | Out-String) -TaskName 'start-dotfiles'"], shell=True)
    common.launch_command("pwsh -Command Install-Module -Name AudioDeviceCmdlets -Force -Verbose", "installation of AudioDeviceCmdlets module")

def install_pywal():
    """
    Installs the pywal package and its dependencies.
    """
    common.install_pckgs(common.EInstaller.PIP, ["pywal", "colorz", "colorthief", "haishoku"])
    print(f"\n === Importing and running" + common.PURPLE + " winwal " + common.NC + "module to the powershell 7 === \n")
    subprocess.run("pwsh -Command update-winwal " + str(common.WINDOTFILES_ASSETS) + "\snow.jpg", text=True)


def create_sym_links(symlink_file: str, system_path: str = ""):
    """
    Creates a symbolic link to the specified file or folder.

    Args:
        symlink_file (str): The name of the file or folder to create the link to.
        system_path (str, optional): The path of the system folder to create the link in.
    """
    print(f"Symlinking {common.PURPLE + symlink_file + common.NC + ' file'}")

    system_file_path = Path(system_path) if system_path else common.HOME / symlink_file
    dotfiles_file_path = common.WINDOTFILES / symlink_file

    assert dotfiles_file_path.is_file() or dotfiles_file_path.is_dir(), "Trying to symlink an invalid dotfiles file/folder!"

    if system_file_path.is_file():
        os.remove(system_file_path)
    else:
        path_parent_folder = system_file_path.parent
        if not path_parent_folder.is_dir():
            os.mkdir(path_parent_folder)

    os.symlink(dotfiles_file_path, system_file_path)


def main():
    """
    The main function of the script.
    """
    input("Pre-installation ready, press enter to continue with the setup. >")

    common.change_win_color_mode()
    prepare_powershell()

    #TODO: 
    # OneCommander: Colors
    # RIDER: Colors
    # Flow launcher: Colors
    # Spicetify (text): setup and colors
    # Discord: colors and themes
    # remove onedrive and pre-installed spotify bro and proper install fro spotify
    # CI/CD github 
    # Fix Windows terminal not closing on startup
    # Create and show somehow shortcuts for used programms such as Glaze, VSCode, Rider etc....
    # Change shortcuts code to match Rider's 

    common.install_pckgs(common.EInstaller.WINGET, common.REQUIRED_WINGET_PROGRAMS)
    
    result = subprocess.run('pwsh -Command $PROFILE', shell=True, capture_output=True, text=True)
    create_sym_links("pwsh/Microsoft.PowerShell_profile.ps1", result.stdout.strip())
    create_sym_links("wt/settings.json", str(common.APPDATA_LOCAL) + "\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json")
    create_sym_links(".glaze-wm/config.yaml")

    common.reload_powershell()

    # Copying flow_launcher windotfiles settings to the computer installation.
    common.launch_command("pwsh -Command cp_windotfiles_to_fl") 

    install_pywal()

    common.install_optional_pckgs(common.EInstaller.WINGET, common.OPTIONAL_WINGET_PROGRAMS)

    create_sym_links("vscode/settings.json", str(common.APPDATA_ROAMING) + "\Code\\User\settings.json")

    common.install_optional_pckgs(common.EInstaller.CODE, [
        "s-nlf-fh.glassit",
        "ms-vscode.cpptools",
        "naumovs.color-highlight",
        "donjayamanne.python-extension-pack",
        "1YiB.rust-bundle",
        "dlasagno.wal-theme",
        "ms-vscode.powershell",
        "eamodio.gitlens",
        "wayou.vscode-todo-highlight",
        "vscode-icons-team.vscode-icons",
        "TabNine.tabnine-vscode",
        "yzhang.markdown-all-in-one"], " --force")

    #TODO: Is this reload necessary?
    common.reload_powershell()
    common.launch_glazewm()

    input("Press enter to close the window. >")


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        logging.error("You should launch the install.bat script as admin!")
        input("Press enter to close the window. >")
    else:
        main()
