"""
Installs all the tools, packages and config symlinks for a new development environment.
Uses the Windows Package Manager (winget) and pip.

Usage:
    python install.py

No admin needed, but creating symlinks on Windows requires Developer Mode
(Settings > Privacy & security > For developers > Developer Mode = On). The script
checks for this up front and tells you if it's missing.

Note: requires an internet connection and may prompt you to accept EULAs.
"""

import os
import sys
import subprocess
from pathlib import Path

# Bootstrap our own dependencies before importing them, so a bare `python install.py`
# works on a fresh machine with nothing but Python installed.
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-q", "-r", str(Path(__file__).with_name("requirements.txt"))],
    check=False,
)

import shutil
import common


def set_windows_options():
    print(f"\n === Battery options: Set to never sleep never hibernate === \n")
    subprocess.run("pwsh -NoProfile -Command powercfg -change -standby-timeout-ac 0", shell=True)
    subprocess.run("pwsh -NoProfile -Command powercfg -change -monitor-timeout-ac 0", shell=True)

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

ZEBAR_WIDGET = "mushfikurr.overline-zebar@1.0.0"

def copy_zebar_widgets():
    dest = str(common.APPDATA_ROAMING) + "\\zebar\\downloads\\" + ZEBAR_WIDGET
    src = str(common.WINDOTFILES) + "\\.config\\glazewm\\zebar\\" + ZEBAR_WIDGET
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(src, dest)

def can_symlink() -> bool:
    """Probe whether this account may create symlinks (admin or Developer Mode)."""
    probe = common.WINDOTFILES / ".symlink_probe"
    link = common.WINDOTFILES / ".symlink_probe.link"
    try:
        probe.write_text("")
        link.unlink(missing_ok=True)
        os.symlink(probe, link)
        return True
    except OSError:
        return False
    finally:
        link.unlink(missing_ok=True)
        probe.unlink(missing_ok=True)

def main():
    """
    The main function of the script.
    """
    if not can_symlink():
        print("This setup creates symlinks, which needs Windows Developer Mode (or admin).")
        print("Enable it: Settings > Privacy & security > For developers > Developer Mode = On, then re-run.")
        input("Press enter to close the window. >")
        return

    input("Pre-installation ready, press enter to continue with the setup. >")

    # winwal (the color engine) is a PowerShell module, so let it import per-user (no admin needed).
    subprocess.run("pwsh -NoProfile -Command Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force", shell=True)
    common.change_win_color_mode()
    set_windows_options()
    common.reload_powershell()

    common.install_pckgs(common.EInstaller.WINGET, common.REQUIRED_WINGET_PROGRAMS)
    common.reload_powershell()

    create_sym_links(".config/wezterm/wezterm.lua", str(common.HOME) + "\\.config\\wezterm\\wezterm.lua")
    create_sym_links(".config/wezterm/winwal.toml", str(common.HOME) + "\\.config\\wezterm\\colors\\winwal.toml")
    create_sym_links(".config/glazewm/config.yaml", str(common.HOME) + "\\.glzr\\glazewm\\config.yaml")
    create_sym_links(".config/glazewm/zebar/settings.json", str(common.HOME) + "\\.glzr\\zebar\\settings.json")
    create_sym_links(".config/nushell/config.nu", str(common.APPDATA_ROAMING) + "\\nushell\\config.nu")
    create_sym_links(".config/flowlauncher/Settings.json", str(common.APPDATA_ROAMING) + "\\FlowLauncher\\Settings\\Settings.json")
    create_sym_links(".config/flameshot.ini", str(common.APPDATA_ROAMING) + "\\flameshot\\flameshot.ini")
    create_sym_links(".config/fastfetch/config.jsonc", str(common.HOME) + "\\.config\\fastfetch\\config.jsonc")
    copy_zebar_widgets()

    common.reload_powershell()

    install_pywal()
    common.install_optional_pckgs(common.EInstaller.WINGET, common.OPTIONAL_WINGET_PROGRAMS)
    common.reload_powershell()

    common.launch_command("glazewm")
    
    input("Press enter to close the window. >")

if __name__ == "__main__":
    main()
