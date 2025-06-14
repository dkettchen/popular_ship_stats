from re import sub

def separate_change_symbol(change_str:str):
    """
    separates input string into a two item list

    converts any numbers into int

    unifies all "New"/"N"/"***" values into "New"

    ie "+3" -> 3
    
    ie "***" -> "New"
    """

    if change_str in ["N", "New", "***", "N*", "Re-Entry"]:
        new_value = "New"
    elif change_str in ["None"]:
        new_value = None
    elif "-" in change_str:
        new_value = - int(sub(r"-", "", change_str))
    elif "+" in change_str:
        new_value = int(sub(r"\+", "", change_str))
    elif change_str.isnumeric():
        new_value = int(change_str)
    else: print(change_str)

    return new_value