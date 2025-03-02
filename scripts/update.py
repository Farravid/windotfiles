"""
This script is used to update all the necessary tools and packages for a the actual development environment.
It uses the Windows Package Manager (winget) and Python's package installer (pip) to install the required software.

Usage:
1. Run the script with python.

"""

import common

def main():
    """
    The main function of the script.
    """

    common.install_pckgs(common.EInstaller.WINGET_UPDGRADE, common.REQUIRED_WINGET_PROGRAMS)
    common.install_optional_pckgs(common.EInstaller.WINGET_UPDGRADE, common.OPTIONAL_WINGET_PROGRAMS)
    common.launch_command("code --update-extensions", "update for VSCode extensions", True)

    input("Press enter to close the window. >")

if __name__ == "__main__":
    main()