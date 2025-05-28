import pandas as pd
from src.cleaning_code_refactor.stage_01_parsing_raw_data import parse_txt
from src.cleaning_code_refactor_utils.find_RPF import find_RPF
from src.cleaning_code_refactor_utils.clean_fandom_labels import clean_fandoms
from src.cleaning_code_refactor_utils.clean_char_names import clean_names
from json import dump

def gather_chars_and_fandoms(data_dict:dict):
    """
    takes a nested dictionary from parsing stage

    returns a dictionary containing all raw fandom names (as keys)
    and the raw character names appearing with them (as list values)
    """

    chars_and_fandoms = {}
    
    # iterating over all files
    years_in_order = sorted(list(data_dict.keys()))
    for year in years_in_order:

        # retrieve all of that year's data
        all_rankings_list = []
        for ranking in data_dict[year]: # go through all rankings of that year
            data_df = data_dict[year][ranking] # relevant ranking df
            all_rankings_list.append(data_df)
        year_rankings = pd.concat(all_rankings_list).reset_index() # combine all rankings into one df
        year_rankings.pop("index")

        # extract all unique fandoms & clean em
        # year_rankings = pd.DataFrame(year_rankings["Fandom"].unique(), columns=["Fandom"])
        year_rankings = find_RPF(year_rankings)
        year_rankings["New Fandom"] = year_rankings["Fandom"].apply(clean_fandoms)

        # go through fandoms
        for row in year_rankings.index:
            current_row = year_rankings.loc[row]
            # print(current_row)
            fandom = current_row["New Fandom"]
            old_fandom = current_row["Fandom"]
            rpf_bool = bool(current_row["RPF"]) # why not regular bool usually smh

            # if it's new, mark it with year joined & rpf status
            if fandom not in chars_and_fandoms.keys():
                chars_and_fandoms[fandom] = {
                    "year_joined": year, 
                    "rpf": rpf_bool, 
                    "raw_versions": [], 
                    "characters": {},
                }

            if rpf_bool != chars_and_fandoms[fandom]["rpf"]:
                chars_and_fandoms[fandom]["rpf"] = "both"

            # if raw version of it is new, add it to list
            if old_fandom not in chars_and_fandoms[fandom]["raw_versions"]:
                chars_and_fandoms[fandom]["raw_versions"].append(old_fandom)

        # put characters in relevant fandoms
        for row in year_rankings.index:
            current_relationship = year_rankings.loc[row, "Relationship"]
            current_fandom = year_rankings.loc[row, "New Fandom"]

            # iterate over all characters in relationship
            for char in current_relationship:
                # clean name
                clean_char = clean_names(char, current_fandom)
                full_name = clean_char["full_name"]

                # if new character
                if full_name not in chars_and_fandoms[current_fandom]["characters"].keys():
                    chars_and_fandoms[current_fandom]["characters"][full_name] = clean_char
                    chars_and_fandoms[current_fandom]["characters"][full_name]["year_joined"] = year
                    chars_and_fandoms[current_fandom]["characters"][full_name]["raw_versions"] = []

                # if old name has not been tracked yet
                if char not in chars_and_fandoms[current_fandom]["characters"][full_name]["raw_versions"]:
                    chars_and_fandoms[current_fandom]["characters"][full_name]["raw_versions"].append(char)

    # checking that all fandoms have characters in them
    for fandom in chars_and_fandoms:
        if len(chars_and_fandoms[current_fandom]["characters"]) == 0:
            print(fandom)

    return chars_and_fandoms



if __name__ == "__main__":
    parsed_dict = parse_txt()
    gathered_dict = gather_chars_and_fandoms(parsed_dict)
    filepath = "data/reference_and_test_files/refactor_helper_files/cleaned_fandoms_and_characters.json"
    with open(filepath, "w") as json_file:
        dump(gathered_dict, json_file, indent=4)
