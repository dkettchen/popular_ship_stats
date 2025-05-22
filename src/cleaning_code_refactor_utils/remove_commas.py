from re import split

def remove_commas(number_str:str):
    """
    turns input into comma-less number
    """

    if "," in number_str:
        num = int("".join(split(r",", number_str)))
    else: num = int(number_str)

    return num

