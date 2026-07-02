import os
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
    Regenerate the overline-zebar palette from the pywal colors.

    overline-zebar applies its theme as inline CSS variables on :root, so a
    stylesheet with !important overrides whatever theme is selected in its UI.
    We write that stylesheet into each widget's assets dir; index.html links it.
    """
    c = [line.rstrip("\r\n") for line in get_color_lines()]

    theme = {
        "--border":            c[8],
        "--background":        c[0],
        "--background-deeper": brighten_color(c[0], 0.6),  # darker
        "--button":            c[8],
        "--button-border":     brighten_color(c[8], 1.3),
        "--primary":           c[4],
        "--primary-border":    c[12],
        "--primary-text":      c[15],
        "--text":              c[7],
        "--text-muted":        c[8],
        "--icon":              c[7],
        "--success":           c[2],
        "--danger":            c[1],
        "--warning":           c[3],
    }

    css = ":root {\n" + "".join(
        f"  {k}: {v} !important;\n" for k, v in theme.items()
    ) + "}\n"

    widget_pkg = "mushfikurr.overline-zebar@1.0.0"
    link = '<link rel="stylesheet" href="./assets/winwal.css">'
    # The repo copy is the committed source; install.py copies it into the live
    # downloads dir (no symlink), so write both — downloads is what zebar serves.
    packs = [
        common.WINDOTFILES / ".config" / "glazewm" / "zebar" / widget_pkg,
        common.APPDATA_ROAMING / "zebar" / "downloads" / widget_pkg,
    ]
    for pack in packs:
        for widget in ("main", "system-stats"):
            dist = pack / "widgets" / widget / "dist"
            if not dist.is_dir():
                continue
            (dist / "assets" / "winwal.css").write_text(css, encoding="utf8")
            index = dist / "index.html"
            html = index.read_text(encoding="utf8")
            if "winwal.css" not in html:
                index.write_text(html.replace("</head>", f"    {link}\n  </head>", 1), encoding="utf8")

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

    # oh-my-posh caches the parsed theme, so running shells keep the old prompt
    # colors until the cache is cleared; then the next prompt re-reads the new omp.json.
    common.launch_command("oh-my-posh cache clear", "a cache clear so running shells repaint the prompt")

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