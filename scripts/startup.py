"""
Logon launcher: starts GlazeWM, asks which setup to open, launches its apps and
moves each window to its workspace.

Setups are TOML templates in scripts/setups/. Each file is one selectable setup;
add a file, get a new choice. Nothing is launched unless you pick a setup.
Edit setups with the GUI: `python setup_editor.py`.

Run `python startup.py --check` to validate every setup file without launching.
"""

import sys
import time
import json
import ctypes
import tomllib
import subprocess
from pathlib import Path

import inquirer

import common

PURPLE = '\033[0;35m'
NC = '\033[0m'

SETUPS_DIR = Path(__file__).parent / "setups"


def load_setups() -> dict[str, list[dict]]:
    """Map setup name (file stem) -> list of app dicts, read from setups/*.toml."""
    setups = {}
    for path in sorted(SETUPS_DIR.glob("*.toml")):
        apps = tomllib.loads(path.read_text(encoding="utf-8")).get("apps", [])
        for app in apps:
            missing = {"launch", "process", "workspace"} - app.keys()
            if missing:
                raise ValueError(f"{path.name}: app {app!r} missing keys {missing}")
        setups[path.stem] = apps
    return setups


def glazewm_running() -> bool:
    """True if a GlazeWM instance is already up (the IPC query answers)."""
    try:
        return subprocess.run(["glazewm", "query", "windows"],
                              capture_output=True, timeout=5).returncode == 0
    except Exception:
        return False


def process_running(image_name: str) -> bool:
    """True if a process with this exe name (e.g. 'buttery-taskbar.exe') is running."""
    try:
        out = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {image_name}"],
                             capture_output=True, text=True, timeout=5).stdout
        return image_name.lower() in out.lower()
    except Exception:
        return False


def get_window_id(process_name: str):
    """Return the GlazeWM window id for a running process, or None."""
    try:
        result = subprocess.run(["glazewm", "query", "windows"], capture_output=True, text=True, check=True)
        windows = json.loads(result.stdout).get("data", {}).get("windows", [])
        for window in windows:
            if window.get("processName") == process_name:
                return window.get("id")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def move_window_to_workspace(process_name, workspace):
    """Move a process's window to a workspace via GlazeWM (no-op if not open)."""
    window_id = get_window_id(process_name)
    if window_id is None:
        print(f"No open window for '{process_name}', skipping move")
        return
    try:
        subprocess.run(["glazewm", "command", "--id", window_id, "move", "--workspace", str(workspace)], check=True)
        print(f"Moved window {window_id} to workspace {workspace}")
    except Exception as e:
        print(f"Error moving window: {e}")


def launch_setup(name: str, apps: list[dict]):
    """Launch every app in a setup, wait for windows, then move them to workspaces."""
    print(f"{PURPLE}== Setup: {name} =={NC}")
    for app in apps:
        common.launch_command(app["launch"], app.get("name", app["process"]))
    time.sleep(5)
    for app in apps:
        move_window_to_workspace(app["process"], app["workspace"])


def main():
    ctypes.windll.kernel32.SetConsoleTitleW("Startup")

    subprocess.Popen("fastfetch", shell=True)
    time.sleep(1.5)

    setups = load_setups()

    print(f"{PURPLE}" * 60 + NC)
    for name, apps in setups.items():
        print(f"{name}: " + ", ".join(app.get("name", app["process"]) for app in apps))
    print(f"{PURPLE}" * 60 + NC)

    answer = inquirer.prompt([
        inquirer.List('choice', message="Select a setup to open:", choices=[*setups, "None"])
    ])
    update = inquirer.confirm("Update windotfiles first (Default=No)?", default=False)

    if update:
        common.launch_command('python %USERPROFILE%/windotfiles/scripts/update.py', "Updating windotfiles", True)
    if answer['choice'] != "None":
        launch_setup(answer['choice'], setups[answer['choice']])


def check():
    """Validate every setup file; exit non-zero on the first bad one."""
    try:
        setups = load_setups()
    except (ValueError, tomllib.TOMLDecodeError) as e:
        print(f"Invalid setup: {e}")
        sys.exit(1)
    for name, apps in setups.items():
        print(f"OK  {name}: {len(apps)} app(s)")
    print(f"{len(setups)} setup(s) valid")


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
        sys.exit(0)
    if glazewm_running():
        print("GlazeWM already running, not launching another instance")
    else:
        common.launch_command("start glazewm")
    if process_running("buttery-taskbar.exe"):
        print("Buttery Taskbar already running, not launching another instance")
    else:
        common.launch_command("start /b " + str(common.WINDOTFILES / Path("vendor/buttery-taskbar2/buttery-taskbar.exe")))
    common.launch_command("glazewm command set-floating && glazewm command size --width 900 --height 900")
    main()
