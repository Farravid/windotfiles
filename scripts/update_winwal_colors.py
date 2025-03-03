import os
import ctypes
import subprocess
import sys
import logging
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

def import_dygma():
    colors_path = Path.home() / ".cache/wal/colors"
    dygma_main = Path.home() / "windotfiles/dygma/dygma_api/src/main.rs"

    erase(dygma_main, "//$", "//&")

    file_read = open(colors_path, "r", encoding="utf8")

    color_lines = file_read.readlines()
    file_read.close()
    
    palette : str = "const COLOR_PALETTE : &str = \""
    line_prepender(dygma_main, "//&")
    for l in color_lines:
        line_to_write = str(ImageColor.getrgb(l[:-1]) + (100,))
        line_to_write = line_to_write.replace("(", "").replace(")", "").replace(",", "")
        palette += line_to_write + " "
    
    palette = palette[:-1] + "\";"
    line_prepender(dygma_main, palette)
    line_prepender(dygma_main, "//$")

def import_glazewm():
    colors_path = Path.home() / ".cache/wal/colors"
    glaze_config_paht = Path.home() / "windotfiles/.config/glazewm/config.yaml"

    erase(glaze_config_paht, "#$", "#&")

    file_read = open(colors_path, "r", encoding="utf8")

    color_lines = file_read.readlines()
    file_read.close()
    
    count = 1
    line_prepender(glaze_config_paht, "#&")
    for l in color_lines:
        line_to_write = "define: &color_" + str(count) + " '" + l[:-1] + "'\n"
        count+=1 
        line_prepender(glaze_config_paht, line_to_write)
    line_prepender(glaze_config_paht, "#$")

def import_wezterm():
    colors_path = Path.home() / ".cache/wal/colors"
    wezterm_colors = Path.home() / "windotfiles/.config/wezterm/winwal.toml"

    file_read = open(colors_path, "r", encoding="utf8")
    color_lines = file_read.readlines()
    file_read.close()

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

def update_winwal():
    """
    Update the color scheme and apply it to the currently active terminal.
    """

    wallpaper_path = os.path.abspath(sys.argv[1])

    # Apply the wallpaper using Windows API for persistence
    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)
    common.launch_command(f"pwsh -Command Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop' -Name WallPaper -Value '{wallpaper_path}'", "Applying Wallpaper")

    common.launch_command(
        f"pwsh -Command Update-WalTheme -Backend colorz -Image {wallpaper_path}",
        "Update-WalTheme to update color schemes with the given wallpaper", True
    )
    import_dygma()
    import_wezterm()

    common.launch_command(
        f"pwsh -Command cargo run --manifest-path $env:USERPROFILE\\windotfiles\\dygma\\dygma_api\\Cargo.toml --release",
        "rust script for applying colors to dygma",
    )

    neofetch_image_path = str(common.WINDOTFILES_ASSETS) + "\\neofetch.png" 
    common.launch_command(f"magick {wallpaper_path} -gravity Center -crop 1200x1200+0+0 +repage {neofetch_image_path}", "an update for fastfetch image")
    common.launch_command("glazewm command wm-redraw", "a reload for GlazeWM")

def main():
    update_winwal()
    subprocess.Popen("fastfetch", shell=True)

if __name__ == "__main__":
    wallpaper_path = Path(os.path.abspath(sys.argv[1]))
    if wallpaper_path.exists():
        main()
    else:
        logging.error(f"{wallpaper_path} does not exist")