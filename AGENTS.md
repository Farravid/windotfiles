# windotfiles

Personal Windows 11 dotfiles: terminal (WezTerm + Nushell), tiling WM
(GlazeWM + Zebar), and a pywal-based color pipeline (winwal, a PowerShell module
used only as a backend — PowerShell is not an interactive shell here). Windows-only.

**The repo must live at `%USERPROFILE%\windotfiles`** — paths across the scripts and
configs are hardcoded to that location.

## Layout

- `.config/` — the actual dotfiles, symlinked into place by `install.py`
  (WezTerm, Nushell, GlazeWM/Zebar, Flow Launcher, Flameshot, fastfetch).
- `scripts/` — Python setup/runtime tooling (see below).
- `vendor/` — third-party bits: `winwal` (git submodule), Buttery Taskbar, ColorTool.
- `assets/` — wallpapers. `readme/` — docs media.
- `start-windotfiles.xml` — Task Scheduler task that runs `startup.bat` on logon.

## Scripts (`scripts/`)

- `install.py` — one-time setup: winget packages, symlinks, pywal. Run with
  `python install.py` (no admin; installs its own deps; needs Developer Mode for symlinks).
- `uninstall.py` — reverses `install.py`: symlinks, Zebar widget, logon task, and
  (after confirmation) the winget/pip packages. Leaves Windows preferences and optional apps alone.
- `update.py` — upgrades winget packages + pip.
- `update_winwal_colors.py` — regenerates the palette from a wallpaper and writes
  `.config/wezterm/winwal.toml` (WezTerm reads this live and re-themes on reload).
- `startup.py` — logon launcher: starts GlazeWM, prompts for a setup, arranges windows.
  Setups are TOML files in `scripts/setups/` (one per file, each lists apps + workspaces).
- `setup_editor.py` — PySide6 GUI to create/edit those setups: pick a program from
  Explorer (icon + processName auto-grabbed), set its workspace (`python setup_editor.py`).
  Themed from the live pywal palette.
- `common.py` — shared paths, the winget package lists, and helpers.

Python deps are pinned in `scripts/requirements.txt` (`inquirer`, `pillow`); `install.py` installs them itself.

## Conventions

- `common.EInstaller` wraps the winget/pip command prefixes.
- Personal, machine-specific values (extra aliases, save paths) don't belong in the
  committed configs — keep them local.
