#########################################
# FUNCTIONS
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