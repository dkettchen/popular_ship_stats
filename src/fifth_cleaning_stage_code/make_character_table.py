from json import load

def make_sorted_char_dict():
    """
    reads the assigning_race_4_assigning_race.json file

    returns a sorted unnested dict of its values with keys made up of "fandom - character", 
    values of the character dicts with an added rpf_or_fic key
    """

    base_demographics_filepath = "data/reference_and_test_files/assigning_demographic_info/assigning_race_4_assigning_race.json"
    with open(base_demographics_filepath, "r") as demo_file:
        loaded_chars = load(demo_file)

    new_dict = {}

    for category in ["RPF", "fictional"]:
        for fandom in loaded_chars[category]:
            for character in loaded_chars[category][fandom]:
                key_name = f"{fandom} - {character}" # alternatively change this format around idk
                new_dict[key_name] = loaded_chars[category][fandom][character]
                new_dict[key_name]["rpf_or_fic"] = category

    sorted_keys = sorted(list(new_dict.keys()))
    sorted_dict = {}

    for key in sorted_keys:
        sorted_dict[key] = new_dict[key]

    return sorted_dict

def prep_characters_for_csv(sorted_dict):
    """
    takes sorted dict from make sorted char dict

    returns a nested list of the column names and the relevant values except for op_versions
    """

    columns = [
        "given_name",
        "middle_name",
        "maiden_name",
        "surname",
        "alias",
        "nickname",
        "title (prefix)",
        "title (suffix)",
        "name_order",
        "full_name",
        "fandom",
        "gender",
        "race",
        "rpf_or_fic"
    ]
    new_list = [columns]

    for key in sorted_dict:
        temp_list = []
        for column in columns:
            temp_list.append(sorted_dict[key][column])
        new_list.append(temp_list)
    
    return new_list



# second char func:
# prep previous output dict for csv:
    # remove op versions key
    # make columns list
    # make values lists for each key
    # add to nested list
    # return nested list

# print to csv using util


