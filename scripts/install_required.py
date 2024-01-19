import os
import subprocess
from pathlib import Path

Purple = '\033[0;35m'
NC = '\033[0m'

# TODO: Check if this is working
windotfiles_path : Path = Path.home() / "windotfiles/"

##
def prepare_powershell():
    print("\n === Installing the last version of module" + Purple + " PSReadLine " + NC + " === \n")
    #subprocess.run("pwsh -Command Install-Module PSReadLine -force", shell=True)
    print("\n === Setting the execution policy for powershell scripts for this user to " + Purple + " RemoteSigned " + NC + " === \n")
    #subprocess.run("pwsh -Command Set-ExecutionPolicy RemoteSigned -Scope CurrentUser", shell=True, text=True)
    print("\n === Importing the " + Purple + " Start-Dotfiles-Farravid.xml " + NC + " task to the Task Scheduler === \n")
    subprocess.run(["pwsh", "-Command", f"Register-ScheduledTask -Xml (Get-Content '{windotfiles_path}\\tasks\\Start-WM.xml' | Out-String) -TaskName 'Start-Dotfiles-Farravid'"], shell=True)

##
##
def install_pcks(installer : str, pkg_names : [str]) -> bool:
    for pkg_name in pkg_names:
        print("\n === Installing " + Purple + pkg_name + NC + " with " + installer + " === \n")
        subprocess.run([installer, "install", pkg_name])

##
##
def install_pywal():
    install_pcks("pip", ["pywal", "colorz", "colorthief", "haishoku"])
    print("\n === Importing and running" + Purple + " winwal " + NC + "module to the powershell 7 === \n")
    subprocess.run("pwsh -Command Update-WalTheme -Image " + windotfiles_path + "/assets/pink-trees.jpeg", text=True)

##
##
def create_sym_links(symlink_file : str, system_path : str = ""):
    print("Symlinking " + Purple + symlink_file + NC + " file")

    system_file_path : Path = Path(system_path) if system_path != "" else Path.home() / symlink_file
    dotfiles_file_path : Path = windotfiles_path / symlink_file

    assert dotfiles_file_path.is_file() or dotfiles_file_path.is_dir(), "Trying to symlink an invalid dotfiles file/folder!"

    if system_file_path.is_file():
        os.remove(system_file_path)
    else:
        path_parent_folder = system_file_path.parent
        if not path_parent_folder.is_dir(): os.mkdir(path_parent_folder)
    
    os.symlink(dotfiles_file_path, system_file_path)

## TODO: REMOVE Eventually here
def launch_app(command, app_name, time_to_sleep = 0.0, workspace = ""):
    print(f"{Purple} == Launching {app_name} == {NC}")
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    #time.sleep(time_to_sleep)

    #if(workspace):
    #   subprocess.Popen(f"i3-msg 'move container to workspace {workspace}'", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

##
def main():
    prepare_powershell()
    # result = subprocess.run('pwsh -Command $PROFILE', shell=True, capture_output=True, text=True)
    # create_sym_links("pwsh/Microsoft.PowerShell_profile.ps1", result.stdout.strip())
    # create_sym_links("wt/settings.json", os.environ['LocalAppData'] + "\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json")
    # create_sym_links(".glaze-wm/config.yaml")
    # install_pcks("winget", ["glazewm",
    #                         "Git.Git",
    #                         "Github.GitLFS",
    #                          "DEVCOM.JetBrainsMonoNerdFont",
    #                          "Microsoft.PowerShell",
    #                          "Microsoft.WindowsTerminal",
    #                          "Microsoft.PowerToys",
    #                          "Microsoft.NuGet",
    #                          "JanDeDobbeleer.OhMyPosh"])
    # subprocess.run("pwsh --Command Invoke-Expression $PROFILE", shell=True)
    # install_pcks("pip", ["inquirer"])
    # install_pywal()

    # glaze_colors_script_path = windotfiles_path / "scripts/import_winwal_glaze_colors.py"
    # launch_app("python " + str(glaze_colors_script_path), "script for reloading colors for GlazeWM from winwal")
    # launch_app("start glazewm", "Glaze (Tilling Windows Manager)")

if __name__ == "__main__":
    main()