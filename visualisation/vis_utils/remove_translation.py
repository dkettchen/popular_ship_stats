from re import split

def remove_translation(fandom_string:str):
    """
    takes a fandom string containing a "|" separator (= that has a translation)

    returns a new string with the translation and the separator removed, 
    leaving only the english title
    """

    split_string = split(r"\s\|\s", fandom_string)

    return split_string[0]