from pathlib import Path
from PIL import ImageColor
import common

def main():
    colors_path = Path.home() / ".cache/wal/colors"
    dygma_main = Path.home() / "windotfiles/dygma/dygma_api/src/main.rs"

    common.erase(dygma_main, "//$", "//&")

    file_read = open(colors_path, "r", encoding="utf8")

    color_lines = file_read.readlines()
    file_read.close()
    
    palette : str = "const COLOR_PALETTE : &str = \""
    common.line_prepender(dygma_main, "//&")
    for l in color_lines:
        line_to_write = str(ImageColor.getrgb(l[:-1]) + (100,))
        line_to_write = line_to_write.replace("(", "").replace(")", "").replace(",", "")
        palette += line_to_write + " "
    
    palette = palette[:-1] + "\";"
    common.line_prepender(dygma_main, palette)
    common.line_prepender(dygma_main, "//$")

if __name__ == "__main__":
    main()