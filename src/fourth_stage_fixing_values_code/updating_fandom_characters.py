from src.util_functions.retrieve_data_from_json_lines import get_json_lines_data
from src.util_functions.get_file_paths import find_paths
from json import dump, load

def collect_characters_by_unified_fandoms():
    """
    updates the full_characters_per_fandom file with unified fandoms
    """

    all_paths = find_paths("data/third_clean_up_data/")

    with open("data/reference_and_test_files/unified_full_fandoms_list.json", "r") as fandoms_file:
        loaded_fandom_dict = load(fandoms_file) # loading dict of all unified fandoms
    
    # separating out the two new categories
    RPF_dict = loaded_fandom_dict["RPF"]
    fic_dict = loaded_fandom_dict["fictional"]

    # making new empty dict for later
    fandom_characters = {
        "RPF": {},
        "fictional": {}
    }
    # adding all fandom keys
    for fandom in RPF_dict:
        fandom_characters["RPF"][fandom] = set()
    for fandom in fic_dict:
        fandom_characters["fictional"][fandom] = set()

    for path in all_paths:
        data_list = get_json_lines_data(path) # getting ranking data

        for row in data_list:
            relationship = row["Relationship"]
            unformatted_fandom = row["Fandom"]
            for key in RPF_dict:
                OP_fandoms = RPF_dict[key]["OP Versions"]
                if unformatted_fandom in OP_fandoms:
                    for character in relationship:
                        fandom_characters["RPF"][key].add(character)
                #else: print(unformatted_fandom, path)
            for key in fic_dict:
                OP_fandoms = fic_dict[key]["OP Versions"]
                if unformatted_fandom in OP_fandoms:
                    for character in relationship:
                        fandom_characters["fictional"][key].add(character)
                #else: print(unformatted_fandom, path)

    # converting sets to sorted lists
    for fandom_key in RPF_dict:
        fandom_characters["RPF"][fandom_key] = sorted(list(fandom_characters["RPF"][fandom_key]))
    for fandom_key in fic_dict:
        fandom_characters["fictional"][fandom_key] = sorted(list(fandom_characters["fictional"][fandom_key]))

    with open("data/reference_and_test_files/full_characters_per_fandom.json", "w") as json_file:
        dump(fandom_characters, json_file, indent=4)


if __name__ == "__main__":
    collect_characters_by_unified_fandoms()
