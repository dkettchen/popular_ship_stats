from re import sub

def remove_equals(rank_str:str):
    """
    removes "=" from given string if any and turns into number
    """

    if "=" in rank_str:
        rank = int(sub("=", "", rank_str))
    else: 
        rank = int(rank_str)

    return rank