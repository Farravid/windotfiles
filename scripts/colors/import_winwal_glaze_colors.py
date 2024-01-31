from pathlib import Path
import common_colors

def main():
    colors_path = Path.home() / ".cache/wal/colors"
    glaze_config_paht = Path.home() / "windotfiles/.glaze-wm/config.yaml"

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

if __name__ == "__main__":
    main()