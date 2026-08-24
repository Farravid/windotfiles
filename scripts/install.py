"""
Installs all the tools, packages, config symlinks and the logon task for a new
development environment. Uses the Windows Package Manager (winget) and pip.

Usage:
    python install.py

Run this elevated: registering the logon task needs admin. Everything else
works unelevated, but creating symlinks on Windows requires Developer Mode
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
import inquirer
import common


def set_windows_options():
    print(f"\n === Battery options: Set to never sleep never hibernate === \n")
    subprocess.run("pwsh -NoProfile -Command powercfg -change -standby-timeout-ac 0", shell=True)
    subprocess.run("pwsh -NoProfile -Command powercfg -change -monitor-timeout-ac 0", shell=True)

def set_yazi_file_env():
    """yazi needs file(1) for MIME detection (text/image previews); Git ships it but not on PATH."""
    print(f"\n === Pointing " + common.PURPLE + "YAZI_FILE_ONE" + common.NC + " at Git's file.exe (yazi previews) === \n")
    file_exe = common.PROGRAM_FILES / "Git" / "usr" / "bin" / "file.exe"
    os.environ["YAZI_FILE_ONE"] = str(file_exe)  # this process
    subprocess.run(f'setx YAZI_FILE_ONE "{file_exe}"', shell=True)  # persistent (user)

def install_audio_cmdlets():
    """Module behind the GlazeWM alt+a audio-toggle binding (see config.yaml)."""
    print(f"\n === Installing the module" + common.PURPLE + " AudioDeviceCmdlets " + common.NC + "(alt+a audio toggle) === \n")
    subprocess.run("pwsh -NoProfile -Command Install-Module AudioDeviceCmdlets -Scope CurrentUser -Force", shell=True)

def install_pywal():
    """
    Installs the pywal package and its dependencies.
    """
    common.install_pckgs(common.EInstaller.PIP, common.PIP_PACKAGES)
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

    if not dotfiles_file_path.exists():
        # Optional tools (hermes) don't always ship a config here. Skipping one
        # symlink shouldn't abort a run that already installed every program.
        print(f"Skipping {common.PURPLE + symlink_file + common.NC}: not in the repo")
        return

    is_dir = dotfiles_file_path.is_dir()

    if system_file_path.is_symlink() or system_file_path.is_file(): os.remove(system_file_path)
    elif system_file_path.is_dir(): shutil.rmtree(system_file_path)
    else: os.makedirs(system_file_path.parent, exist_ok=True)

    print(f"Symlinking {common.PURPLE + symlink_file + common.NC + ' to ' + common.PURPLE + str(system_file_path) + common.NC}")
    os.symlink(dotfiles_file_path, system_file_path, target_is_directory=is_dir)

def copy_zebar_widgets():
    """
    Zebar v3 finds custom packs one level down from its config dir
    (~/.glzr/zebar/<pack>/zpack.json), taking the pack id from that zpack.json's
    "name" field. %APPDATA%/zebar/downloads is where v2 kept marketplace
    downloads; v3 resolves those through installer metadata instead, so a pack
    copied there is never found and the bar dies on startup with
    "No widget pack found for ..." in ~/.glzr/zebar/errors.log.
    """
    dest = common.HOME / ".glzr" / "zebar" / common.ZEBAR_PACK_ID
    src = common.WINDOTFILES / ".config" / "glazewm" / "zebar" / common.ZEBAR_WIDGET
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(src, dest)

def install_hermes_agent():
    """
    Hermes agent (NousResearch), optional: it isn't on winget so it runs their
    install script, and it ships no config of its own in this repo.
    """
    question = [
        inquirer.List(
            "choice",
            "Do you want to install " + common.PURPLE + "Hermes agent" + common.NC + " ?",
            ["Yes", "No"],
        ),
    ]
    if inquirer.prompt(question)["choice"] != "Yes":
        return

    print(f"\n === Installing " + common.PURPLE + "Hermes agent" + common.NC + " (NousResearch) === \n")
    subprocess.run("pwsh -NoProfile -Command irm https://hermes-agent.nousresearch.com/install.ps1 | iex", shell=True)

def register_startup_task():
    """Registers the logon task that runs startup.bat (replaces the manual Task Scheduler import)."""
    print(f"\n === Registering the " + common.PURPLE + "Start windotfiles" + common.NC + " logon task === \n")
    result = subprocess.run(f'schtasks /Create /XML "{common.WINDOTFILES / "start-windotfiles.xml"}" /TN "Start windotfiles" /F',
                            shell=True, capture_output=True, text=True)
    print(result.stdout or result.stderr)
    if result.returncode != 0:
        # This used to fail mutely, so a run that never registered the task
        # still ended on "All done" and the launcher just never came up.
        print(f"{common.PURPLE}Could not register the logon task{common.NC} -- schtasks needs "
              f"an elevated terminal. Re-run install.py as administrator, or register it "
              f"by hand from one.")

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
    if shutil.which("winget") is None:
        print("winget is missing or broken. Fix it first: https://github.com/microsoft/winget-cli/issues/3832")
        input("Press enter to close the window. >")
        return

    if not can_symlink():
        print("This setup creates symlinks, which needs Windows Developer Mode (or admin).")
        print("Enable it: Settings > Privacy & security > For developers > Developer Mode = On, then re-run.")
        input("Press enter to close the window. >")
        return

    input("Pre-installation ready, press enter to continue with the setup. >")

    # In case the repo was cloned without --recurse-submodules.
    subprocess.run("git submodule update --init --recursive", shell=True, cwd=common.WINDOTFILES)

    # PowerShell 7 (pwsh) backs everything below, so it goes first.
    common.install_pckgs(common.EInstaller.WINGET, ["Microsoft.PowerShell"])
    common.reload_powershell()

    # winwal (the color engine) is a PowerShell module, so let it import per-user (no admin needed).
    subprocess.run("pwsh -NoProfile -Command Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force", shell=True)
    common.change_win_color_mode()
    set_windows_options()
    install_audio_cmdlets()
    common.reload_powershell()

    common.install_pckgs(common.EInstaller.WINGET, common.REQUIRED_WINGET_PROGRAMS)
    common.reload_powershell()
    set_yazi_file_env()

    for repo_file, system_path in common.SYMLINKS:
        create_sym_links(repo_file, str(system_path))
    copy_zebar_widgets()

    npm_dir = common.HOME / ".config/opencode"
    if (npm_dir / "package.json").is_file():
        print(f"\n === Installing " + common.PURPLE + "opencode npm dependencies" + common.NC + " === \n")
        common.launch_command(f"npm install --prefix {npm_dir}", "opencode npm dependencies", True)

    common.reload_powershell()

    install_pywal()
    common.install_optional_pckgs(common.EInstaller.WINGET, common.OPTIONAL_WINGET_PROGRAMS)
    install_hermes_agent()
    common.reload_powershell()

    register_startup_task()

    common.launch_command("glazewm")

    print("\nAll done. Reboot to fully apply the changes.")
    input("Press enter to close the window. >")

if __name__ == "__main__":
    main()
