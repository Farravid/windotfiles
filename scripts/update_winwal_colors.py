import os
import re
import hashlib
import ctypes
import subprocess
import shlex
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from PIL import ImageColor
from colorsys import rgb_to_hsv, hsv_to_rgb
import common

#########################################
# HELPER FUNCTIONS
#########################################

def line_prepender(filename: str, line: str) -> None:
    """
    This function prepends a line to the beginning of a file.

    Args:
        filename (str): The name of the file.
        line (str): The line to prepend.

    Returns:
        None

    Raises:
        ValueError: If the file does not exist.
    """
    if not os.path.exists(filename):
        raise ValueError(f"The file '{filename}' does not exist")

    with open(filename, 'r+', encoding="utf8") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

#########################################
# IMPORTERS
######################################### 

def get_color_lines():
    colors_path = Path.home() / ".cache/wal/colors"

    file_read = open(colors_path, "r", encoding="utf8")
    color_lines = file_read.readlines()
    file_read.close()

    return color_lines

def brighten_color(hex_color, factor=1.3):
    """
    Takes a hex color and returns a brighter version.
    factor > 1 increases brightness, factor < 1 decreases it.
    """
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    h, s, v = rgb_to_hsv(r, g, b)
    v = min(1.0, v * factor)  # Increase brightness but keep within valid range
    r, g, b = hsv_to_rgb(h, s, v)
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

def import_winwal_brights():
    colors_path = Path.home() / ".cache/wal/colors"
    with open(colors_path, "r") as f:
        colors = [line.strip() for line in f.readlines() if line.strip()]
    
    if len(colors) != 16:
        raise ValueError("Expected 16 colors in the file")
    
    ansi_colors = colors[:8]
    bright_colors = [colors[8]] + [brighten_color(color, 1.5) for color in colors[9:]]

    with open(colors_path, "w") as f:
        for color in ansi_colors + bright_colors:
            f.write(color + "\n")
            
def import_wezterm():
    wezterm_colors = Path.home() / "windotfiles/.config/wezterm/winwal.toml"
    color_lines = get_color_lines()

    # Cleaning up the file
    open(wezterm_colors, 'w').close()

    brights_colors_str = ""
    for brights_index in range(8, 16):
        brights_colors_str += "\"" + color_lines[brights_index][:-1] + "\"" + ","
    brights_colors_str = brights_colors_str[:-1] 
    line_prepender(wezterm_colors, "brights = [" + brights_colors_str + "]")

    ansi_colors_str = ""
    for ansi_index in range(0, 8):
        ansi_colors_str += "\"" + color_lines[ansi_index][:-1] + "\"" + ","
    ansi_colors_str = ansi_colors_str[:-1] 
    line_prepender(wezterm_colors, "ansi = [" + ansi_colors_str + "]")

    line_prepender(wezterm_colors, "selection_fg = \""     + color_lines[6][:-1] + "\"")
    line_prepender(wezterm_colors, "selection_bg = \""     + color_lines[5][:-1] + "\"")
    line_prepender(wezterm_colors, "cursor_fg = \""        + color_lines[4][:-1] + "\"")
    line_prepender(wezterm_colors, "cursor_border = \""    + color_lines[3][:-1] + "\"")
    line_prepender(wezterm_colors, "cursor_bg = \""        + color_lines[2][:-1] + "\"")
    line_prepender(wezterm_colors, "background = \""       + color_lines[0][:-1] + "\"")
    line_prepender(wezterm_colors, "foreground = \""       + color_lines[7][:-1] + "\"")
    line_prepender(wezterm_colors, "[colors]")

def import_zebar():
    """
    Regenerate the sakura zebar palette from the pywal colors.

    sakura ships its theme as CSS variables on :root (with a .light override),
    so a stylesheet using !important wins over whichever of the two is active.
    We write that stylesheet next to the pack's own assets; index.html links it.

    The repo copy is the committed source; install.py copies it into
    ~/.glzr/zebar (no symlink), so write both -- the latter is what zebar serves.
    """
    c = [line.rstrip("\r\n") for line in get_color_lines()]

    theme = {
        "--bg-main":      c[0],
        "--text-main":    c[7],
        "--accent":       c[4],
        "--workspace-bg": c[4],
    }

    css = ":root {\n" + "".join(
        f"  {k}: {v} !important;\n" for k, v in theme.items()
    ) + "}\n"

    # The webview caches local assets, so the link carries a digest of the
    # palette to bust that cache whenever the colors actually change.
    stamp = hashlib.sha1(css.encode("utf8")).hexdigest()[:8]
    link = f'<link rel="stylesheet" href="./assets/winwal.css?v={stamp}">'

    packs = [
        common.WINDOTFILES / ".config" / "glazewm" / "zebar" / common.ZEBAR_PACK_ID,
        common.HOME / ".glzr" / "zebar" / common.ZEBAR_PACK_ID,
    ]
    for pack in packs:
        if not pack.is_dir():
            print(f"No zebar pack at {common.PURPLE}{pack}{common.NC}, skipping it")
            continue
        for index in pack.glob("**/dist/index.html"):
            assets = index.parent / "assets"
            if not assets.is_dir():
                continue
            (assets / "winwal.css").write_text(css, encoding="utf8")
            html = index.read_text(encoding="utf8")
            # Drop the link a previous run left behind, then re-add it stamped.
            html = re.sub(r'[ \t]*<link rel="stylesheet" href="\./assets/winwal\.css[^"]*">\r?\n', "", html)
            html = re.sub(r'([ \t]*)</head>', lambda m: f"{m[1]}{link}\n{m[1]}</head>", html, count=1)
            index.write_text(html, encoding="utf8")

#####################################################################
## Actual winwal update
####################################################################

def update_winwal(wallpaper_path):
    """
    Update the color scheme and apply it to the currently active terminal.
    """

    # Apply the wallpaper using Windows API for persistence
    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)
    common.launch_command(f"pwsh -NoProfile -Command Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop' -Name WallPaper -Value '{wallpaper_path}'", "Applying Wallpaper")

    # winwal is a PowerShell module. Import it inline so this works without a PS profile
    # (we no longer symlink one — WezTerm + Nushell is the only interactive shell).
    winwal_module = common.WINDOTFILES / "vendor" / "winwal" / "winwal.psm1"
    common.launch_command(
        f"pwsh -NoProfile -Command \"Import-Module '{winwal_module}'; Update-WalTheme -Backend colorz -Image {wallpaper_path}\"",
        "Update-WalTheme to update color schemes with the given wallpaper", True
    )
    
    import_winwal_brights()
    import_wezterm()
    import_zebar()

    neofetch_image_path = str(common.WINDOTFILES_ASSETS) + "\\neofetch.png"
    common.launch_command(f"magick {wallpaper_path} -gravity Center -crop 1200x1100+0+0 +repage {neofetch_image_path}", "an update for fastfetch image")

    # Kill Zebar first: reloading the config relaunches it (config_reload_commands),
    # but launching zebar.exe while it's already running no-ops (single instance),
    # so the widgets never re-read the regenerated winwal.css without a fresh start.
    common.launch_command('taskkill /IM zebar.exe /F', "a kill for Zebar so the reload relaunches it fresh")
    common.launch_command("glazewm command wm-reload-config", "a reload for GlazeWM and Zebar")

def main():        
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(title="Select an Image, you can select it from windotfiles assets", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

    if file_path:
        safe_path = shlex.quote(file_path)
        update_winwal(safe_path)
        subprocess.Popen("fastfetch", shell=True)

if __name__ == "__main__":
    main()