import pandas as pd
from src.cleaning_code_refactor.stage_01_parsing_raw_data import parse_txt
from src.cleaning_code_refactor_utils.find_RPF import find_RPF
from src.cleaning_code_refactor_utils.clean_fandom_labels import clean_fandoms
from src.cleaning_code_refactor_utils.clean_char_names import clean_names
from json import dump
from data.reference_and_test_files.refactor_helper_files.folder_lookup import LOOKUPS_ETC

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

# clean actual ranking names -> new version of the input dict with clean name columns
def clean_rankings(data_dict:dict):
    """
    takes a nested dictionary from parsing stage

    returns a new nested dict with each ranking df where
    - Fandom and Relationship columns have been renamed to "Old ~"
    - new Fandom and Relationship columns have been added with the respective cleaned names
    - Member 1 through 4 columns have been added with the names of the respective member 
    (same order as original relationship), 
    with Member 3 and 4 being None if there are less members
    - an RPF column has also been added
    """

    new_dict = {}
    
    # iterating over all files
    years_in_order = sorted(list(data_dict.keys()))
    for year in years_in_order:
        new_dict[year] = {}
        for ranking in data_dict[year]:

            data_df = data_dict[year][ranking].copy() # relevant ranking df

            # add rpf column
            data_df = find_RPF(data_df)

            # clean fandoms
            data_df["New Fandom"] = data_df["Fandom"].apply(clean_fandoms)

            # clean relationships
            new_relationship_column = []
            for row in data_df.index:
                current_row = data_df.loc[row]
                old_relationship = current_row["Relationship"]
                fandom = current_row["New Fandom"]
                new_relationship = [clean_names(name, fandom)["full_name"] for name in old_relationship]
                new_relationship_column.append(new_relationship)
            data_df["New Relationship"] = new_relationship_column
            data_df["Member 1"] = [row[0] for row in new_relationship_column]
            data_df["Member 2"] = [row[1] for row in new_relationship_column]
            data_df["Member 3"] = [row[2] if len(row) > 2 else None for row in new_relationship_column]
            data_df["Member 4"] = [row[3] if len(row) > 3 else None for row in new_relationship_column]

            # rename columns
            renaming_dict = {
                "Fandom" : "Old Fandom",
                "New Fandom" : "Fandom",
                "Relationship" : "Old Relationship",
                "New Relationship" : "Relationship",
            }
            data_df = data_df.rename(columns=renaming_dict)

            # add cleaned df
            new_dict[year][ranking] = data_df

    return new_dict

    # return chars_and_fandoms

# I guess our lookups function as old name - new name files

if __name__ == "__main__":
    parsed_dict = parse_txt()
    gathered_dict = gather_chars_and_fandoms(parsed_dict)
    cleaned_ranking_dict = clean_rankings(parsed_dict)
