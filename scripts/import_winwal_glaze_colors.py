from pathlib import Path

## This function will delete all line from the givin start_key
## until the stop_key. (include: start_key) (exclude: stop_key)
## 
def erase(file_name: str, start_key: str, stop_key: str):
    try: 
        with open(file_name, 'r+', encoding="utf8") as fr: 
            lines = fr.readlines()

        with open(file_name, 'w+', encoding="utf8") as fw:
            delete = False
            was_last_line = False
            for line in lines:
                if line.strip('\n') == start_key: delete = True
                elif line.strip('\n') == stop_key: delete = False
                
                if not delete and was_last_line: fw.write(line)
                if not delete: was_last_line = True
            
    except RuntimeError as ex: 
        print(f"erase error:\n\t{ex}")

##
##
def line_prepender(filename, line):
    with open(filename, 'r+', encoding="utf8") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def main():
    colors_path = Path.home() / ".cache/wal/colors"
    glaze_config_paht = Path.home() / "windotfiles/.glaze-wm/config.yaml"

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

if __name__ == "__main__":
    main()