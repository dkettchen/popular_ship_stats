from re import split

def sort_race_combos(input_list:list):
    """
    takes a list of unique race tag combos (ie "White / E Asian")

    returns a dict where any combos that were not already in alphabetical order have a key
    of the original combo tag, and a value of the alphabetically ordered version
    """
    rename_dict = {}

    for combo in input_list:
        sorted_split_version = sorted(split(r"\s\/\s", combo))
        reconcat_version = sorted_split_version[0]
        for item in sorted_split_version[1:]:
            reconcat_version += " / " + item
        if reconcat_version != combo:
            rename_dict[combo] = reconcat_version

    return rename_dict
