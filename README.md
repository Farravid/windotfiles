<div align="center">
  <h1>windotfiles</h1>
  <img src="https://custom-icon-badges.demolab.com/badge/Windows%2011-0078D6?style=for-the-badge&logo=windows11&logoColor=white"</img>
  <img alt="Static Badge" src="https://img.shields.io/badge/glazewm-A9225C?style=for-the-badge&logoColor=white">
  <img alt="Static Badge" src="https://img.shields.io/badge/zebar-654FF0?style=for-the-badge&logoColor=white">
  <img alt="Static Badge" src="https://img.shields.io/badge/wezterm-4E49EE?style=for-the-badge&logo=wezterm&logoColor=white">
  <img alt="Static Badge" src="https://img.shields.io/badge/nushell-4E9A06?style=for-the-badge&logo=nushell&logoColor=white">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"</img>
  <p></p>  

</div>

<div align="center">
  <img src="readme/showcase.gif" alt="Showcase of the windotfiles opening terminals, bottom and using update-winwal"/>
  <p>
    <sub>
      Showcase of the windotfiles opening terminals, bottom and using update-winwal.
    </sub>
  </p>
</div>

# Table of Contents
- [Repository explanation](#repository-explanation)
- [Installation](#installation)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. WinGet](#2-winget)
  - [3. Python and Microsoft PowerShell 7](#3-python-and-microsoft-powerShell-7)
  - [4. Dependencies](#4-dependencies)
  - [5. Run the script](#5-run-the-script)
  - [6. Configure the Task Scheduler](#4-configure-the-task-scheduler)
  - [7. Reboot the system](#5-reboot-the-system)
- [Usage](#usage)
  - [Startup launcher](#startup-launcher)
  - [Update the color scheme](#update-the-color-scheme)
- [Credits](#credits)

# Repository explanation
> [!WARNING]
 💀 Working in Windows is hard 💀

As you may know, at least for developers, Linux tends to be easier than Windows but Windows is the standard, at least for the videogames industry.\
Tired of setting up Windows again and again on different machines or fresh installs I have decided to create a permanent way of keeping my changes and my setup.

On top of that, I'm decided to speed up my productivity with a window tilling manager similar to i3 on Linux 🌟 `GlazeWM` 🌟 and some other cool features and automatizations.  

# Installation
In this section we will describe all the necessary steps to install the windotfiles 

## 1. Clone the repository
Using the following command to clone the repository with `PowerShell`
```shell
cd $env:USERPROFILE 
git clone --recurse-submodules https://github.com/Farravid/windotfiles.git
```

This will clone the repository and also recursively clone the submodules.
> [!WARNING]
If you don't clone the repository in the user's home directory, the setup won't work at all.\
Most of the setup depends on this.

## 2. WinGet
The main pre-requisite is to have the `WinGet` package manager operative. It should be available on the lastest Windows versions.

Nevertheless, and it is no surprise, `WinGet` could not work as expected with a fresh windows installation.\
If you end up having the blue stuck problem visit this issue: https://github.com/microsoft/winget-cli/issues/3832, specially the following code:
```
Invoke-WebRequest -Uri https://aka.ms/getwinget -OutFile winget.msixbundle
Add-AppPackage -ForceApplicationShutdown .\winget.msixbundle
del .\winget.msixbundle
```

## 3. Python and Microsoft PowerShell 7

This windotfiles repository uses `Python` and `PowerShell` for some of the functionalities.
We need to make sure those are installed on the system.
> [!WARNING]
Python should be installed from winget, not from Microsoft Store. Make sure to use the same commands described here.

```
winget install Python.Python.3.13
winget install Microsoft.PowerShell
```

This should be enough to begin with the installation.

## 4. Dependencies
In order to fully install and use the windotfiles, you need to install some dependencies.\
Some dependencies are mandatory for a basic windotfiles installation but others are optional since they are just preferences.

You can check the list of dependencies in the files `scripts/common`.
You will find it under `REQUIRED` and `OPTIONAL WINGET_PROGRAMS`

## 5. Run the script
Go to the **windotfiles** folder and run the `install.bat` batch script as **ADMIN**
> [!WARNING]
Windotfiles won't work if you don't run the script as admin

## 6. Configure the Task Scheduler

> [!WARNING]
Adding the `start-dotfiles` task to the **Task Scheduler** is optional but recommended for faster inits.
Using the startup folder will be slower and less user friendly.

The windotfiles repository includes a `start-dotfiles.xml` that must be used to configure the **Task Scheduler** to start the dotfiles automatically on log on.
This task is in charge of launching the [`Startup launcher`](#startup-launcher) that will launch the setup.

![alt text](readme/task-scheduler.png)

## 7. Reboot the system

After completing the previous steps, restart the system to fully apply the changes.

# Usage
After the successful installation, you can still modify the windotfiles for your specific cases or use some of the functionalities described below.

## Startup launcher
This python script (`startup.py`) will be launched from the `Task Scheduler` every time you log in. It is in charge of launching `GlazeWM` and prompting the user with a setup selector.

Once the user has selected the setup and the default apps, that setup will be launched.

The default configuration is the basic configuration and but you can feel free of changing it in order to match your purposes and setups.

![alt text](readme/startup.png)

> [!NOTE]
Make sure to disable all the relevant programs from windows start up in order to have a perfect experience

## Update the color scheme
In top of winwal, we have an `update-winwal` powershell command available for updating the color scheme based on the given wallpaper.\
This command, for now, supports updating the color scheme of the following software:
- `Windows Terminal`
- `Wezterm`

# Credits
- [`GlazeWM`](https://github.com/glzr-io/glazewm)
- [`Winwal`](https://github.com/scaryrawr/winwal)
- [`Buttery Taskbar 2`](https://github.com/LuisThiamNye/ButteryTaskbar2)
- [`Oh My Posh`](https://ohmyposh.dev/)
- [`Flow Launcher`](https://www.flowlauncher.com/)
