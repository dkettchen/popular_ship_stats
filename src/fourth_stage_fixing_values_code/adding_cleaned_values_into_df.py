from src.util_functions.get_file_paths import find_paths
from src.fourth_stage_fixing_values_code.extracting_clean_abbr_name_lists import (
    extract_clean_character_names, 
    extract_clean_fandom_names
)
from json import load, dump
from copy import deepcopy

def run_stage_4_cleaning(): 
    abbr_names_dict = extract_clean_character_names()
    abbr_fandoms_dict = extract_clean_fandom_names()

    all_paths = find_paths("data/third_clean_up_data/")

    for path in all_paths: # going through all the files
        with open(path, "r") as data_file:
            dict_list = load(data_file) # list of dicts

        new_list = []
        for row in dict_list: # row is a dict

            new_row = deepcopy(row) # transferring all values

            for fandom in abbr_fandoms_dict:
                if row["Fandom"] in abbr_fandoms_dict[fandom]:
                    new_row["Old Fandom"] = new_row["Fandom"] # storing prior version
                    new_row["Fandom"] = fandom # replacing fandom
                    break # we found fandom, we don't need to keep looking
                elif row["Fandom"] == 'Star Wars Story (2016)':
                    new_row["Old Fandom"] = "Rogue One: A Star Wars Story (2016)"
                    new_row["Fandom"] = "Star Wars"
                    
            
            new_row["Old Characters"] = new_row["Relationship"] # renaming, keeping order intact
            new_row["Relationship"] = [] # emptying list


            for character in row["Relationship"]:
                for new_character in abbr_names_dict[new_row["Fandom"]]:
                    if character in abbr_names_dict[new_row["Fandom"]][new_character]["op_versions"]:
                        new_row["Relationship"].append(new_character)
                        new_row["RPF or Fic"] = abbr_names_dict[new_row["Fandom"]][new_character]["rpf_or_fic"]
                            # should be same label for all char involved if I did my job right
                        break # should only break innermost loop, so continue to next char
        
            new_row["Relationship"] = sorted(new_row["Relationship"]) # sorting alphabetically

            new_list.append(new_row)
        
        folder_name = path[25:33]
        specific_file = path[34:-5]

        file_name = f"data/fourth_clean_up_data/{folder_name}/{specific_file}.json"

        with open(file_name, "w") as target_file:
            dump(new_list, target_file, indent=4)


if __name__ == "__main__":
    run_stage_4_cleaning()
    pass