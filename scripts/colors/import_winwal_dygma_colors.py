from pathlib import Path
from PIL import ImageColor
import common

def main():
    colors_path = Path.home() / ".cache/wal/colors"
    glaze_config_paht = Path.home() / "windotfiles/dygma/dygma_api/src/main.rs"

    common.erase(glaze_config_paht, "//$", "//&")

    file_read = open(colors_path, "r", encoding="utf8")

    color_lines = file_read.readlines()
    file_read.close()
    
    count = 1
    palette : str = "const COLOR_PALETTE : &str = \""
    common.line_prepender(glaze_config_paht, "//&")
    for l in color_lines:
        line_to_write = str(ImageColor.getrgb(l[:-1]) + (100,))
        line_to_write = line_to_write.replace("(", "").replace(")", "").replace(",", "")
        #line_to_write = "//const color_" + str(count) + " : &str = \"" + l[:-1] + "\";\n"
        count+=1
        palette += line_to_write + " "
        #line_prepender(glaze_config_paht, line_to_write)
    
    palette = palette[:-1] + "\";"
    common.line_prepender(glaze_config_paht, palette)
    common.line_prepender(glaze_config_paht, "//$")

if __name__ == "__main__":
    main()