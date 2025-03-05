import os
import ctypes
import subprocess
import shlex
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from PIL import ImageColor
import common

#########################################
# HELPER FUNCTIONS
#########################################

def erase(file_name: str, start_key: str, stop_key: str):
    """
    This function erases the content between two given keys in a file.

    Args:
        file_name (str): The name of the file.
        start_key (str): The start key.
        stop_key (str): The stop key.

    Returns:
        None

    Raises:
        RuntimeError: If an error occurs.
    """
    try:
        with open(file_name, 'r+', encoding="utf8") as fr:
            lines = fr.readlines()

        with open(file_name, 'w+', encoding="utf8") as fw:
            delete = False
            was_last_line = False
            for line in lines:
                if line.strip('\n') == start_key: delete = True
                elif line.strip('\n') == stop_key: delete = False

                if not delete and was_last_line:
                    fw.write(line)
                if not delete:
                    was_last_line = True

    except RuntimeError as ex:
        print(f"erase error:\n\t{ex}")

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

def import_dygma():
    dygma_main = Path.home() / "windotfiles/dygma/dygma_api/src/main.rs"
    erase(dygma_main, "//$", "//&")

    color_lines = get_color_lines()
    
    palette : str = "const COLOR_PALETTE : &str = \""
    line_prepender(dygma_main, "//&")
    for l in color_lines:
        line_to_write = str(ImageColor.getrgb(l[:-1]) + (100,))
        line_to_write = line_to_write.replace("(", "").replace(")", "").replace(",", "")
        palette += line_to_write + " "
    
    palette = palette[:-1] + "\";"
    line_prepender(dygma_main, palette)
    line_prepender(dygma_main, "//$")

def import_zebar():
    zebar_colors = Path.home() / "windotfiles/.config/glazewm/zebar/config.yaml"
    color_lines = get_color_lines()

    with open(zebar_colors, "r", encoding="utf8") as file:
        content = file.readlines()

    # Replace the line if it contains the search string
    content = ["      --rp-text: " + color_lines[1][:-1]+ ";" + "\n" if "--rp-text:" in line else line for line in content]
    content = ["      --rp-love: " + color_lines[2][:-1]+ ";" + "\n" if "--rp-love:" in line else line for line in content]
    content = ["      --rp-gold: " + color_lines[3][:-1]+ ";" + "\n" if "--rp-gold:" in line else line for line in content]
    content = ["      --rp-rose: " + color_lines[4][:-1]+ ";" + "\n" if "--rp-rose:" in line else line for line in content]
    content = ["      --rp-pine: " + color_lines[5][:-1]+ ";" + "\n" if "--rp-pine:" in line else line for line in content]
    content = ["      --rp-foam: " + color_lines[6][:-1]+ ";" + "\n" if "--rp-foam:" in line else line for line in content]
    content = ["      --rp-iris: " + color_lines[7][:-1]+ ";" + "\n" if "--rp-iris:" in line else line for line in content]

    # Write the modified content back to the file
    with open(zebar_colors, "w", encoding="utf8") as file:
        file.writelines(content)

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

#####################################################################
## Actual winwal update
####################################################################

def update_winwal(wallpaper_path, is_fastfetch_photo):
    """
    Update the color scheme and apply it to the currently active terminal.
    """

    # Apply the wallpaper using Windows API for persistence
    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)
    common.launch_command(f"pwsh -Command Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop' -Name WallPaper -Value '{wallpaper_path}'", "Applying Wallpaper")

    common.launch_command(
        f"pwsh -Command Update-WalTheme -Backend colorz -Image {wallpaper_path}",
        "Update-WalTheme to update color schemes with the given wallpaper", True
    )

    import_zebar()
    import_dygma()
    import_wezterm()

    common.launch_command(
        f"pwsh -Command cargo run --manifest-path $env:USERPROFILE\\windotfiles\\dygma\\dygma_api\\Cargo.toml --release",
        "rust script for applying colors to dygma",
    )

    neofetch_image_path = str(common.WINDOTFILES_ASSETS) + "\\neofetch.png"
    if is_fastfetch_photo:
        common.launch_command(f"pwsh -Command cp {wallpaper_path} {neofetch_image_path}", "", True)
    else: 
        common.launch_command(f"magick {wallpaper_path} -gravity Center -crop 1200x1100+0+0 +repage {neofetch_image_path}", "an update for fastfetch image")

    common.launch_command("glazewm command wm-reload-config", "a reload for GlazeWM and Zebar")

def main():        
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

    if file_path:
        safe_path = shlex.quote(file_path)
        fastfetch = tk.messagebox.askyesno("Fastfetch", "Set as fastfetch photo?")
        update_winwal(safe_path, fastfetch)
        subprocess.Popen("fastfetch", shell=True)

if __name__ == "__main__":
    main()