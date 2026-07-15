# windotfiles

Personal Windows 11 dotfiles: terminal (WezTerm + Nushell), tiling WM
(GlazeWM + Zebar), and a pywal-based color pipeline (winwal, a PowerShell module
used only as a backend — PowerShell is not an interactive shell here). Windows-only.

**The repo must live at `%USERPROFILE%\windotfiles`** — paths across the scripts and
configs are hardcoded to that location.

## Public repository — security

**This repository is public.** It is strictly forbidden to commit or submit
anything that could compromise the user's security: API keys, tokens, OAuth
credentials, auth files, session/history databases, or any other
secret-bearing machine state. When in doubt, leave it out and ask.

This especially applies to agent config directories that mix tracked config
with local secrets — e.g. `%LOCALAPPDATA%\hermes\`: only `config.yaml` is
tracked (via `.config/hermes/config.yaml`); `auth.json`, `.env`,
`state.db*`, and its caches must never be added to `SYMLINKS` or committed.
Before staging changes near any agent config, check `git status`/`git diff`
for exactly the files expected.

## Agent workflow

Three agents are in play here: Hermes (local LLM, via Ollama) for everyday
lightweight use, Claude Code (frontier models) for heavier work, and
OpenCode — currently prepped with a local Ollama provider in
`.config/opencode/opencode.jsonc` but not yet the daily driver — as the
eventual replacement once its local-LLM setup is ready.

## Layout

- `.config/` — the actual dotfiles, symlinked into place by `install.py`
  (WezTerm, Nushell, GlazeWM/Zebar, Flow Launcher, Flameshot, fastfetch,
  Hermes's `config.yaml` only — see security note above).
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
