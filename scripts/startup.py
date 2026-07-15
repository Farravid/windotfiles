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


def focus_console():
    """Bring this terminal back to the foreground (launched apps steal focus at logon)."""
    # ponytail: under WezTerm the ConPTY console window is hidden, so target the
    # WezTerm window by class; fall back to the real console if run elsewhere.
    hwnd = (ctypes.windll.user32.FindWindowW("org.wezfurlong.wezterm", None)
            or ctypes.windll.kernel32.GetConsoleWindow())
    if hwnd:
        # ponytail: fake an Alt keypress — Windows blocks SetForegroundWindow
        # from background processes unless a key event is in flight.
        ctypes.windll.user32.keybd_event(0x12, 0, 0, 0)      # Alt down
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        ctypes.windll.user32.keybd_event(0x12, 0, 2, 0)      # Alt up (KEYEVENTF_KEYUP)


def refresh_taskbar():
    """Make the taskbar re-read theme colors (it's created unthemed at logon).

    ponytail: WM_CLOSE-recreating Shell_TrayWnd didn't cure the white flash on
    first Win press — the recreated tray was just as stale. Broadcasting
    ImmersiveColorSet makes Explorer re-read accent colors and repaint in place.
    """
    ctypes.windll.user32.SendMessageTimeoutW(
        0xFFFF, 0x001A, 0, "ImmersiveColorSet",  # HWND_BROADCAST, WM_SETTINGCHANGE
        0x0002, 1000, None)                      # SMTO_ABORTIFHUNG, 1s per window


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


def query_windows() -> list[dict]:
    """Return GlazeWM's current window list (empty on error)."""
    try:
        result = subprocess.run(["glazewm", "query", "windows"], capture_output=True, text=True, check=True)
        return json.loads(result.stdout).get("data", {}).get("windows", [])
    except Exception as e:
        print(f"Error: {e}")
        return []


def move_window(window_id, workspace, label):
    """Move a GlazeWM window to a workspace."""
    try:
        subprocess.run(["glazewm", "command", "--id", window_id, "move", "--workspace", str(workspace)], check=True)
        print(f"Moving {label} to workspace {workspace}")
    except Exception as e:
        print(f"Error moving {label}: {e}")


def launch_setup(name: str, apps: list[dict]) -> list[str]:
    """Launch every app in a setup, moving each window as soon as GlazeWM manages it.

    Returns the processes whose window never appeared within 30s (empty = all launched).
    """
    print(f"{PURPLE}== Setup: {name} =={NC}")
    for app in apps:
        common.launch_command(app["launch"], app.get("name", app["process"]), detached=True)
    # ponytail: 1s poll of the window list instead of a GlazeWM IPC event
    # subscription — same effect within a second, no stream parsing. Upgrade
    # to `glazewm sub -e window_managed` if slow-launching apps need it snappier.
    pending = {app["process"]: app for app in apps}
    deadline = time.time() + 30
    while pending and time.time() < deadline:
        for window in query_windows():
            app = pending.pop(window.get("processName"), None)
            if app is not None:
                move_window(window["id"], app["workspace"], app.get("name", app["process"]))
        if pending:
            time.sleep(1)
    for process in pending:
        print(f"No window appeared for '{process}' within 30s, skipping move")
    subprocess.run(["glazewm", "command", "focus", "--workspace", "1"], check=False)
    return list(pending)


def main():
    ctypes.windll.kernel32.SetConsoleTitleW("Startup")

    subprocess.Popen("fastfetch", shell=True)
    time.sleep(1.5)

    setups = load_setups()

    print(f"{PURPLE}" * 60 + NC)
    for name, apps in setups.items():
        print(f"{name}: " + ", ".join(app.get("name", app["process"]) for app in apps))
    print(f"{PURPLE}" * 60 + NC)

    focus_console()
    answer = inquirer.prompt([
        inquirer.List('choice', message="Select a setup to open:", choices=[*setups, "None"])
    ])
    update = inquirer.confirm("Update windotfiles first (Default=No)?", default=False)

    if update:
        common.launch_command('python %USERPROFILE%/windotfiles/scripts/update.py', "Updating windotfiles", True)
    if answer['choice'] != "None":
        launch_setup(answer['choice'], setups[answer['choice']])
        # Let the script exit so WezTerm closes the window automatically,
        # whether or not every app's window was found in time.


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
    refresh_taskbar()
    common.launch_command("glazewm command set-floating && glazewm command size --width 1000 --height 1000")
    main()
