#########################################
# FUNCTIONS
#########################################

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

## Append a line at the top of a file 
##
def line_prepender(filename, line):
    with open(filename, 'r+', encoding="utf8") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)