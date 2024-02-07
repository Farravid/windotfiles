import os
import subprocess
import sys
import logging

## Adding parent folder (scrips) to the path in order to use common
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import common

def update_dygma_winwal():
    """
    Update the dygma color scheme and apply it to the currently keyboard.

    Args:
        None

    Returns:
        None

    """
    dygma_colors_script_path = common.WINDOTFILES_SCRIPTS / "colors/import_winwal_dygma_colors.py"
    common.launch_command(
        f"python {str(dygma_colors_script_path)}",
        "a reload for dygma color scheme",
    )
    common.launch_command(
        f"pwsh -Command cargo run --manifest-path $env:USERPROFILE\windotfiles\dygma\dygma_api\Cargo.toml --release",
        "rust script for applying colors to dygma",
    )


## Update the winwal colors and the wallpaper
##
def update_winwal():
    """
    Update the color scheme and apply it to the currently active terminal.

    Args:
        wallpaper_path (str): The path to the wallpaper image.

    Returns:
        None

    """
    common.launch_command(
        f"pwsh -Command Update-WalTheme -Image {os.path.abspath(sys.argv[1])}",
        "Update-WalTheme to update color schemes with the given wallpaper",
    )
    #update_dygma_winwal()


def main():
    update_winwal()
    common.launch_command(
        f"pwsh -Command Stop-Process -Name GlazeWM -Force", "a reload for GlazeWM"
    )
    common.launch_glazewm()
    logging.warning("In order to fully update the winwal colors you may need to restart the Windows Terminal")


if __name__ == "__main__":
    main()