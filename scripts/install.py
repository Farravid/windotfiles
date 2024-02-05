import os
import subprocess
import logging
import inquirer
import pyuac
from pathlib import Path
import common

##
def prepare_powershell():
    print("\n === Installing the last version of module" + common.PURPLE + " PSReadLine " + common.NC + " === \n")
    subprocess.run("pwsh -Command Install-Module PSReadLine -force", shell=True)
    print("\n === Setting the execution policy for powershell scripts for this user to " + common.PURPLE + " RemoteSigned " + common.NC + " === \n")
    subprocess.run("pwsh -Command Set-ExecutionPolicy RemoteSigned -Scope CurrentUser", shell=True, text=True)
    print("\n === Importing the " + common.PURPLE + " Start-Dotfiles-Farravid.xml " + common.NC + " task to the Task Scheduler === \n")
    subprocess.run(["pwsh", "-Command", f"Register-ScheduledTask -Xml (Get-Content '{common.WINDOTFILES}\\tasks\\Start-WM.xml' | Out-String) -TaskName 'Start-Dotfiles-Farravid'"], shell=True)

##
##
def install_pckgs(installer : str, pkg_names : [str]) -> bool:
    for pkg_name in pkg_names:
        print("\n === Installing " + common.PURPLE + pkg_name + common.NC + " with " + installer + " === \n")
        subprocess.run([installer, "install", pkg_name])

def install_optional_pckgs(installer : str, pkg_names : [str]):
    for pkg_name in pkg_names:
        
        message = 'Do you want to unstall ' + common.PURPLE + pkg_name + common.NC + ' ?'
        question = [
            inquirer.List(
                "choice", message,["Yes", "No"],
            ),
        ]

        answer = inquirer.prompt(question)

        if answer["choice"] == "Yes":
            install_pckgs(installer, [pkg_name])

##
##
def install_pywal():
    install_pckgs("pip", ["pywal", "colorz", "colorthief", "haishoku"])
    print("\n === Importing and running" + common.PURPLE + " winwal " + common.NC + "module to the powershell 7 === \n")
    #TODO: I cant do the update-winwal thingy because it will kill the terminal
    subprocess.run("pwsh -Command Update-WalTheme -Image " + str(common.WINDOTFILES_ASSETS) + "\pink-trees.jpeg", text=True)

##
##
def create_sym_links(symlink_file : str, system_path : str = ""):
    print("Symlinking " + common.PURPLE + symlink_file + common.NC + " file")

    system_file_path : Path = Path(system_path) if system_path != "" else common.HOME / symlink_file
    dotfiles_file_path : Path = common.WINDOTFILES / symlink_file

    assert dotfiles_file_path.is_file() or dotfiles_file_path.is_dir(), "Trying to symlink an invalid dotfiles file/folder!"

    if system_file_path.is_file():
        os.remove(system_file_path)
    else:
        path_parent_folder = system_file_path.parent
        if not path_parent_folder.is_dir(): os.mkdir(path_parent_folder)
    
    os.symlink(dotfiles_file_path, system_file_path)

##
def main():
    input("Pre-installation ready, press enter to continue with the setup. >")
    prepare_powershell()

    install_pckgs("winget", ["glzr-io.glazewm",
                            "Git.Git",
                            "Github.GitLFS",
                            "DEVCOM.JetBrainsMonoNerdFont",
                            "Microsoft.WindowsTerminal",
                            "Microsoft.PowerToys",
                            "Microsoft.NuGet",
                            "JanDeDobbeleer.OhMyPosh",
                            "neofetch"])

    result = subprocess.run('pwsh -Command $PROFILE', shell=True, capture_output=True, text=True)
    create_sym_links("pwsh/Microsoft.PowerShell_profile.ps1", result.stdout.strip())
    create_sym_links("wt/settings.json", os.environ['LocalAppData'] + "\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json")
    create_sym_links(".glaze-wm/config.yaml")
    
    common.reload_profile()
    
    install_pywal()

    install_optional_pckgs("winget", ["Spotify.Spotify",
                                      "Google.Chrome",
                                      "GitHub.GitHubDesktop",
                                      "Discord.Discord",
                                      "Obsidian.Obsidian",
                                      "voidtools.Everything",
                                      "Microsoft.VisualStudioCode",
                                      "Microsoft.VisualStudio.2022.Community",
                                      "Rustlang.Rustup"])

    common.launch_glazewm()

    common.change_win_color_mode()
    input("Press enter to close the window. >")

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        logging.error("You should launch the pre_install.bat script as admin!")
        input("Press enter to close the window. >")
    else:        
        main()