import os
import subprocess
from pathlib import Path

Purple = '\033[0;35m'
NC = '\033[0m'

def prepare_powershell():
    print("\n === Installing last version of module" + Purple + " PSReadLine " + NC + " === \n")
    subprocess.run("powershell Install-Module PSReadLine -force", shell=True)
    print("\n === Setting the execution policy for powershell scripts for this user to " + Purple + " RemoteSigned " + NC + " === \n")
    subprocess.run("powershell Set-ExecutionPolicy RemoteSigned -Scope CurrentUser", shell=True, text=True)

def install_pcks(installer : str, pkg_names : [str]) -> bool:
    for pkg_name in pkg_names:
        print("\n === Installing " + Purple + pkg_name + NC + " with " + installer + " === \n")
        subprocess.run([installer, "install", pkg_name])

def create_sym_links(symlink_files : [str]):
    for slf in symlink_files:
        print("Symlinking " + Purple + slf + NC + " file")

        system_file_path = Path.home() / slf
        dotfiles_file_path = Path.home() / "windotfiles" / slf

        print(system_file_path)
        print(dotfiles_file_path)
        
        assert dotfiles_file_path.is_file() or dotfiles_file_path.is_dir(), "Trying to symlink an invalid dotfiles file/folder!"

        if system_file_path.is_file():
            pass
            os.remove(system_file_path)
        else:
            path_parent_folder = system_file_path.parent
            if not path_parent_folder.is_dir(): os.mkdir(path_parent_folder)
        
        os.symlink(dotfiles_file_path, system_file_path)

def main():
    prepare_powershell()
    create_sym_links([".glaze-wm/config.yaml"])
    install_pcks("winget", ["glazewm",
                             "DEVCOM.JetBrainsMonoNerdFont",
                             "Microsoft.WindowsTerminal",
                             "Microsoft.PowerToys",
                             "Microsoft.NuGet",
                             "JanDeDobbeleer.OhMyPosh"])
    install_pcks("pip", ["inquirer"])

if __name__ == "__main__":
    main()