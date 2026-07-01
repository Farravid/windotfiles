"""
This script updates all the tools and packages in the current development environment.
It uses the Windows Package Manager (winget) and Python's package installer (pip) to upgrade the software.

Usage:
1. Run the script with python.

"""

import common

def main():
    """
    The main function of the script.
    """
    common.install_pckgs(common.EInstaller.WINGET_UPGRADE, common.REQUIRED_WINGET_PROGRAMS)
    common.launch_command("python -m pip install --upgrade pip", "Upgrading pip", True)
    common.install_optional_pckgs(common.EInstaller.WINGET_UPGRADE, common.OPTIONAL_WINGET_PROGRAMS)

    input("Press enter to close the window. >")

if __name__ == "__main__":
    main()