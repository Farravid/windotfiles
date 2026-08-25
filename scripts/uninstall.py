"""
Reverses install.py: removes the config symlinks, the copied Zebar pack, the
"Start windotfiles" logon task, the YAZI_FILE_ONE env var and (after
confirmation) the winget/pip packages.

Usage:
    python uninstall.py

Deliberately left alone: Windows preferences install.py touched (dark mode,
power settings, execution policy) and the optional apps (Spotify, Discord,
Rider, ...) — uninstalling a browser someone kept using would be worse than
leaving a registry value behind. Delete the repo folder itself afterwards.
"""

import os
import shutil
import subprocess
from pathlib import Path

import common


def main():
    for _, system_path in common.SYMLINKS:
        path = Path(system_path)
        if path.is_symlink():
            print(f"Removing symlink {common.PURPLE}{path}{common.NC}")
            if path.is_dir(): os.rmdir(path)
            else: path.unlink()
        elif path.exists():
            print(f"Keeping {path}: not a symlink (not ours)")

    zebar_pack = common.HOME / ".glzr" / "zebar" / common.ZEBAR_PACK_ID
    if zebar_pack.exists():
        print(f"Removing Zebar pack {common.PURPLE}{zebar_pack}{common.NC}")
        shutil.rmtree(zebar_pack, ignore_errors=True)

    print(f"\n === Removing the {common.PURPLE}Start windotfiles{common.NC} logon task === \n")
    subprocess.run('schtasks /Delete /TN "Start windotfiles" /F', shell=True)
    subprocess.run("reg delete HKCU\\Environment /v YAZI_FILE_ONE /f", shell=True)

    if input("\nAlso uninstall the winget/pip packages? [y/N] > ").strip().lower() == "y":
        for pkg_name in common.REQUIRED_WINGET_PROGRAMS:
            print(f"\n === Uninstalling {common.PURPLE}{pkg_name}{common.NC} === \n")
            subprocess.run(f"winget uninstall {pkg_name}", shell=True)
        subprocess.run("pip uninstall -y " + " ".join(common.PIP_PACKAGES), shell=True)
        subprocess.run("pwsh -NoProfile -Command Uninstall-Module AudioDeviceCmdlets -Force", shell=True)

    print("\nDone. Windows preferences (dark mode, power, execution policy) and optional apps were left as-is.")
    print("Delete this repo folder to finish. Reboot to fully apply the changes.")
    input("Press enter to close the window. >")


if __name__ == "__main__":
    main()
