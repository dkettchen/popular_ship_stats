import pandas as pd
from src.cleaning_code_refactor_utils.find_RPF import find_RPF
from src.cleaning_code_refactor_utils.clean_fandom_labels import clean_fandoms
from src.cleaning_code_refactor_utils.clean_char_names import clean_names
from json import dump
from data.reference_and_test_files.refactor_helper_files.folder_lookup import LOOKUPS_ETC

def gather_raw_chars_and_fandoms(data_dict:dict):
    """
    takes a nested dictionary from parsing stage

    returns a dictionary containing all raw fandom names (as keys)
    and the raw character names appearing with them (as list values)
    """

    chars_and_fandoms = {}
    
    # iterating over all files
    for year in data_dict:
        for ranking in data_dict[year]: 
            data_df = data_dict[year][ranking]

            # get all fandoms
            unique_fandoms = list(data_df["Fandom"].unique()) 

            # add fandom to dict if new
            for fandom in unique_fandoms: 
                if fandom not in chars_and_fandoms:
                    chars_and_fandoms[fandom] = []
            
            # put characters in relevant fandoms
            for row in data_df.index:
                current_relationship = data_df.loc[row, "Relationship"]
                current_fandom = data_df.loc[row, "Fandom"]

                # iterate over all characters in relationship
                for char in current_relationship:
                    # if they're not in their fandom's list yet, add them
                    if char not in chars_and_fandoms[current_fandom]:
                        chars_and_fandoms[current_fandom].append(char)

    # all fandoms should have characters to go with them
    for key in chars_and_fandoms:
        if len(chars_and_fandoms[key]) == 0:
            print(key)

    return chars_and_fandoms

# get by year joined & clean fandoms & characters -> dict & json file
def gather_chars_and_fandoms(data_dict:dict):
    """
    takes a nested dictionary from parsing stage

    returns as well as creates a json file with 
    a dictionary containing all new fandom names (as keys) with 
    - the year they first appeared in the ranking,
    - all years they appeared in,
    - their RPF status (True, False. or "both" (eg if both fictional characters 
    and their actors are in the ranking)),
    - their previous names,
    - and a dict of their characters, 
    which in turn contains 
        - all new character names (as keys)
        - their full name (same as key) ((we are forgoing their full name bits from 
        previous code's version as they're not used after cleaning -> no need to save them)),
        - the year they first appeared in the ranking,
        - all years they appeared in,
        - and their previous names
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
                    "years_appeared": [year],
                    "rpf": rpf_bool, 
                    "raw_versions": [], 
                    "characters": {},
                }

            if rpf_bool != chars_and_fandoms[fandom]["rpf"]:
                chars_and_fandoms[fandom]["rpf"] = "both"

            # if raw version of it is new, add it to list
            if old_fandom not in chars_and_fandoms[fandom]["raw_versions"]:
                chars_and_fandoms[fandom]["raw_versions"].append(old_fandom)
            # if this year's appearance has not been tracked yet
            if year not in chars_and_fandoms[fandom]["years_appeared"]:
                chars_and_fandoms[fandom]["years_appeared"].append(year)

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
                    chars_and_fandoms[current_fandom]["characters"][full_name]["years_appeared"] = [year]
                    chars_and_fandoms[current_fandom]["characters"][full_name]["raw_versions"] = []

                # if old name has not been tracked yet
                if char not in chars_and_fandoms[current_fandom]["characters"][full_name]["raw_versions"]:
                    chars_and_fandoms[current_fandom]["characters"][full_name]["raw_versions"].append(char)
                # if this year's appearance has not been tracked yet
                if year not in chars_and_fandoms[current_fandom]["characters"][full_name]["years_appeared"]:
                    chars_and_fandoms[current_fandom]["characters"][full_name]["years_appeared"].append(year)

    # checking that all fandoms have characters in them
    for fandom in chars_and_fandoms:
        if len(chars_and_fandoms[current_fandom]["characters"]) == 0:
            print(fandom)

    # save clean chars & fandoms to a file
    filepath = f"{LOOKUPS_ETC}/cleaned_fandoms_and_characters.json"
    with open(filepath, "w") as json_file:
        dump(chars_and_fandoms, json_file, indent=4)

    return chars_and_fandoms
