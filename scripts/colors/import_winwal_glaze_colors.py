from pathlib import Path
import common_colors

def main():
    colors_path = Path.home() / ".cache/wal/colors"
    glaze_config_paht = Path.home() / "windotfiles/.config/glazewm/config.yaml"

    common_colors.erase(glaze_config_paht, "#$", "#&")

    file_read = open(colors_path, "r", encoding="utf8")

    color_lines = file_read.readlines()
    file_read.close()
    
    count = 1
    common_colors.line_prepender(glaze_config_paht, "#&")
    for l in color_lines:
        line_to_write = "define: &color_" + str(count) + " '" + l[:-1] + "'\n"
        count+=1 
        common_colors.line_prepender(glaze_config_paht, line_to_write)
    common_colors.line_prepender(glaze_config_paht, "#$")

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
    common_colors.line_prepender(wezterm_colors, "brights = [" + brights_colors_str + "]")

    ansi_colors_str = ""
    for ansi_index in range(0, 8):
        ansi_colors_str += "\"" + color_lines[ansi_index][:-1] + "\"" + ","
    ansi_colors_str = ansi_colors_str[:-1] 
    common_colors.line_prepender(wezterm_colors, "ansi = [" + ansi_colors_str + "]")

    common_colors.line_prepender(wezterm_colors, "selection_fg = \""     + color_lines[6][:-1] + "\"")
    common_colors.line_prepender(wezterm_colors, "selection_bg = \""     + color_lines[5][:-1] + "\"")
    common_colors.line_prepender(wezterm_colors, "cursor_fg = \""        + color_lines[4][:-1] + "\"")
    common_colors.line_prepender(wezterm_colors, "cursor_border = \""    + color_lines[3][:-1] + "\"")
    common_colors.line_prepender(wezterm_colors, "cursor_bg = \""        + color_lines[2][:-1] + "\"")
    common_colors.line_prepender(wezterm_colors, "background = \""       + color_lines[0][:-1] + "\"")
    common_colors.line_prepender(wezterm_colors, "foreground = \""       + color_lines[7][:-1] + "\"")
    common_colors.line_prepender(wezterm_colors, "[colors]")

if __name__ == "__main__":
    import_wezterm()