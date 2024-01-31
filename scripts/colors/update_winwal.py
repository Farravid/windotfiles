import os
import subprocess
import sys

## Adding parent folder (scrips) to the path in order to use common
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import common

## Reimport the colors using the python script and then apply the colors using the Rust API from dygma
##
def update_dygma_winwal():
    dygma_colors_script_path = common.WINDOTFILES_SCRIPTS / "colors/import_winwal_dygma_colors.py"
    common.launch_command("python " + str(dygma_colors_script_path), "a reload for dygma color scheme")
    common.launch_command("pwsh -Command cargo run --manifest-path $env:USERPROFILE\windotfiles\dygma\dygma_api\Cargo.toml --release", "rust script for applying colors to dygma")

## Update the winwal colors and the wallpaper
##
def update_winwal():
    common.launch_command("pwsh -Command Update-WalTheme -Image " + os.path.abspath(sys.argv[1]), "Update-WalTheme to update color schemes with the given wallpaper")
    update_dygma_winwal()

def main():
    update_winwal()
    common.launch_command("pwsh -Command Stop-Process -Name GlazeWM -Force", "a reload for GlazeWM")
    common.launch_glazewm()
    common.launch_command("pwsh -Command Stop-Process -Name WindowsTerminal -Force")
    subprocess.Popen("start /b wt", shell=True)

if __name__ == "__main__":
    main()