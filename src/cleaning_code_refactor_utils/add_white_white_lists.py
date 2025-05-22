def add_white_white_list(race_str:str):
    """
    if the input string is "White", it returns ["White", "White"]

    otherwise it just returns the same as input
    """

    if race_str == "White":
        return ["White", "White"]
    else:
        return race_str