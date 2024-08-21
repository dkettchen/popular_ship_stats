import pandas as pd
from json import load, dump


def extract_clean_character_names():
    """
    returns a nested dict with each character's full name, the prior versions of their name, 
    and their rpf/fic category, organised by fandom (cleaned name) and character ("")
    {
        < fandom >: {
            < character >: {
                "full_name": str,
                "op_versions": list,
                "rpf_or_fic": str ("RPF" or "fictional")
            }, ...
        }, ...
    }
    """

    filepath = "data/reference_and_test_files/cleaning_characters/cleaned_characters_list_5_complete_character_names.json"
    with open(filepath, "r") as complete_chars_file:
        complete_chars = load(complete_chars_file)["complete_characters"]

    abbreviated_characters_by_fandom = {}
    for category in ["RPF", "fictional"]:
        for fandom in complete_chars[category]:
            if fandom not in abbreviated_characters_by_fandom.keys():
                abbreviated_characters_by_fandom[fandom] = {}

            for character in complete_chars[category][fandom]:
                if character in abbreviated_characters_by_fandom[fandom].keys():
                    print(character, fandom)

                full_name = complete_chars[category][fandom][character]["full_name"]
                prior_versions = complete_chars[category][fandom][character]["op_versions"]

                abbreviated_characters_by_fandom[fandom][character] = {
                    "full_name": full_name,
                    "op_versions": prior_versions,
                    "rpf_or_fic": category
                }

    return abbreviated_characters_by_fandom

def extract_clean_fandom_names():
    """
    returns a look up dictionary with clean fandom name keys and op version set values
    {< fandom_name > : {< op_versions >, ...}, ...}
    """

    filepath = "data/reference_and_test_files/cleaning_fandoms/unified_full_fandoms_list.json"
    with open(filepath, "r") as full_fandoms_file:
        full_fandoms = load(full_fandoms_file)

    abbreviated_fandoms = {}
    for category in ["RPF", "fictional"]:
        for fandom in full_fandoms[category]:
            prior_versions = full_fandoms[category][fandom]["OP Versions"]
            if fandom not in abbreviated_fandoms.keys():
                abbreviated_fandoms[fandom] = set(prior_versions) 
                # making a look up dict of clean name : set of op versions
            else: # if the fandom was already in rpf
                for item in prior_versions: # rotate through new op versions
                    abbreviated_fandoms[fandom].add(item) 
                    # add em to the set, 
                    # so they get added if they're new 
                    # & don't fuck us up if they're already in there

    for key in abbreviated_fandoms:
        abbreviated_fandoms[key] = sorted(list(abbreviated_fandoms[key]))
    
    return abbreviated_fandoms



if __name__ == "__main__":
    abbreviated_characters = extract_clean_character_names()
    with open("data/reference_and_test_files/cleaning_characters/unified_abbr_characters_list.json", "w") as unified_characters_file:
        dump(abbreviated_characters, unified_characters_file, indent=4)
    
    abbreviated_fandoms = extract_clean_fandom_names()
    with open("data/reference_and_test_files/cleaning_fandoms/unified_abbr_fandoms_list.json", "w") as unified_fandoms_file:
        dump(abbreviated_fandoms, unified_fandoms_file, indent=4)