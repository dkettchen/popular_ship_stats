def read_txt(filepath:str):
    """
    takes a txt filepath

    returns a list of strings of each line
    """
    with open(filepath, "r") as txt:
        read_data = txt.readlines()
    
    # adding missing newline character
    read_data[-1] += "\n"
    return read_data