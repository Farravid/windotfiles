# windotfiles

Personal Windows 11 dotfiles: terminal (WezTerm + Nushell/PowerShell), tiling WM
(GlazeWM + Zebar), and a pywal-based color pipeline (winwal). Windows-only.

**The repo must live at `%USERPROFILE%\windotfiles`** — paths across the scripts and
configs are hardcoded to that location.

## Layout

- `.config/` — the actual dotfiles, symlinked into place by `install.py`
  (WezTerm, Nushell, PowerShell profile, Windows Terminal, GlazeWM/Zebar,
  Flow Launcher, Flameshot, fastfetch).
- `scripts/` — Python setup/runtime tooling (see below).
- `vendor/` — third-party bits: `winwal` (git submodule), Buttery Taskbar, ColorTool.
- `assets/` — wallpapers. `readme/` — docs media.
- `start-windotfiles.xml` — Task Scheduler task that runs `startup.bat` on logon.

## Scripts (`scripts/`)

- `install.bat` → installs Python deps from `requirements.txt`, then runs `install.py`.
- `install.py` — one-time setup: winget packages, symlinks, pywal. **Run as admin.**
- `update.py` — upgrades winget packages + pip.
- `update_winwal_colors.py` — regenerates the palette from a wallpaper and writes
  `.config/wezterm/winwal.toml` (WezTerm reads this live and re-themes on reload).
- `startup.py` — logon launcher: starts GlazeWM, prompts for a setup, arranges windows.
- `common.py` — shared paths, the winget package lists, and helpers.

Python deps are pinned in `scripts/requirements.txt` (`inquirer`, `pyuac`, `pywin32`, `pillow`).

## Conventions

- `common.EInstaller` wraps the winget/pip command prefixes.
- Personal, machine-specific values (extra aliases, save paths) don't belong in the
  committed configs — keep them local.
