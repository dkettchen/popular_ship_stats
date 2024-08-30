def make_old_names_dict(sorted_dict):
    """
    takes sorted dict from make_sorted_dict

    returns a dict with same keys that only contains the full name, fandom and op versions
    """
    new_dict = {}

    for key in sorted_dict:
        new_char_dict = {
            "full_name" : sorted_dict[key]["full_name"],
            "fandom" : sorted_dict[key]["fandom"],
            "op_versions" : sorted_dict[key]["op_versions"]
        }
        new_dict[key] = new_char_dict
    
    return new_dict

def prep_old_names_for_csv(old_names_dict):
    """
    takes dict of old names from make old names dict func

    returns a nested list with the column names and values where 
    the old names have been unnested into their own rows
    """
    new_list = [["old_name", "full_name", "fandom", "key"]]

    for key in old_names_dict:
        name = old_names_dict[key]["full_name"]
        fandom = old_names_dict[key]["fandom"]
        for old_name in old_names_dict[key]["op_versions"]:
            temp_list = [old_name, name, fandom, key]
            new_list.append(temp_list)

    return new_list