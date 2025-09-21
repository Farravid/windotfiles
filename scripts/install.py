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
    subprocess.run("pwsh -Command Install-Module AudioDeviceCmdlets -force", shell=True)

def install_pywal():
    """
    Installs the pywal package and its dependencies.
    """
    common.install_pckgs(common.EInstaller.PIP, ["pywal", "colorz", "colorthief", "haishoku"])
    print(f"\n === Importing and running" + common.PURPLE + " winwal " + common.NC + "module to the powershell 7 === \n")
    common.launch_command('python %USERPROFILE%/windotfiles/scripts/update_winwal_colors.py')
    
def create_sym_links(symlink_file: str, system_file_path: str):
    """
    Creates a symbolic link to the specified file or folder.

    Args:
        symlink_file (str): The name of the file or folder to create the link to.
        system_path (str, optional): The path of the system folder to create the link in.
    """
    system_file_path = Path(system_file_path)
    dotfiles_file_path = common.WINDOTFILES / symlink_file

    assert dotfiles_file_path.is_file(), "Trying to symlink an invalid dotfiles file!"

    if system_file_path.exists(): os.remove(system_file_path)
    else: os.makedirs(system_file_path.parent, exist_ok=True)
        
    print(f"Symlinking {common.PURPLE + symlink_file + common.NC + ' to ' + common.PURPLE + str(system_file_path) + common.NC}")
    os.symlink(dotfiles_file_path, system_file_path)    

def copy_startup_script_to_startup_directory():
    """
    This function copies the 'startup.bat' script to the Windows startup directory.
    The script is located in the same directory as the current script.
    """
    startup_path = '"' + str(common.APPDATA_ROAMING) + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup" + '"'

    common.launch_command("copy startup.bat " + startup_path)

#TODO:
# we need the shortcuts on nushell rather than powershell
# set monitor and standby to never: powercfg -change -monitor-timeout-ac 0
#  david  powercfg -change -standby-timeout-ac 0
# disable print screen key to open screen capture for flameshot:
# Set-ItemProperty -Path "HKCU:\Control Panel\Keyboard" -Name "PrintScreenKeyForSnippingEnabled" -Value 0
# Investigate settings windows System > For developers
# Wait a bit or event driven moving workspaces
# Zebar themes download and colors
# Create and show somehow shortcuts for used programms such as Glaze, Rider etc....
# Would be awesome to create a rust gui program to create your own startup stuff

def main():
    """
    The main function of the script.
    """
    input("Pre-installation ready, press enter to continue with the setup. >")

    # common.change_win_color_mode()
    # prepare_powershell()
    # common.reload_powershell()
    # 
    # #common.install_pckgs(common.EInstaller.WINGET, common.REQUIRED_WINGET_PROGRAMS)
    # common.reload_powershell()
    # 
    # result = subprocess.run('pwsh -Command $PROFILE', shell=True, capture_output=True, text=True)
    # create_sym_links(".config/Microsoft.PowerShell_profile.ps1", result.stdout.strip())
    # create_sym_links(".config/wt/settings.json", str(common.APPDATA_LOCAL) + "\\Packages\\Microsoft.WindowsTerminal_8wekyb3d8bbwe\\LocalState\\settings.json")
    # create_sym_links(".config/wezterm/wezterm.lua", str(common.HOME) + "\\.config\\wezterm\\wezterm.lua")
    # create_sym_links(".config/wezterm/winwal.toml", str(common.HOME) + "\\.config\\wezterm\\colors\\winwal.toml")
    # create_sym_links(".config/glazewm/config.yaml", str(common.HOME) + "\\.glzr\\glazewm\\config.yaml")
    # create_sym_links(".config/glazewm/zebar/settings.json", str(common.HOME) + "\\.glzr\\zebar\\settings.json")
    # create_sym_links(".config/nushell/config.nu", str(common.APPDATA_ROAMING) + "\\nushell\\config.nu")
    # create_sym_links(".config/flowlauncher/Settings.json", str(common.APPDATA_ROAMING) + "\\FlowLauncher\\Settings\\Settings.json")
    # create_sym_links(".config/flameshot.ini", str(common.APPDATA_ROAMING) + "\\flameshot\\flameshot.ini")
    # create_sym_links(".config/fastfetch/config.jsonc", str(common.HOME) + "\\.config\\fastfetch\\config.jsonc")
    # 
    # common.reload_powershell()

    # TODO: copy_startup_script_to_startup_directory() or add task to task scheduler for fast stuff

    install_pywal()
    #common.install_optional_pckgs(common.EInstaller.WINGET, common.OPTIONAL_WINGET_PROGRAMS)
    common.reload_powershell()

    common.launch_command("glazewm")
    
    input("Press enter to close the window. >")


if __name__ == "__main__":
    # if not pyuac.isUserAdmin():
    #     logging.error("You should launch the install.bat script as admin!")
    #     input("Press enter to close the window. >")
    # else:
        main()
