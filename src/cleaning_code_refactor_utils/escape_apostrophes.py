from re import sub

def escape_apostrophes(input_str:str):
    """
    replaces any apostrophes and double quotes in the given string with a regular apostrophe/single quote

    returns the new version of the string
    """

    new_str = input_str

    for symbol in ["'", '”', "“", "’", '"']:
        if symbol in new_str:
            new_str = sub(symbol, "'", new_str)

    return new_str