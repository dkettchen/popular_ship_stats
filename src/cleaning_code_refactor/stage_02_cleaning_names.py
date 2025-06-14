from src.cleaning_code_refactor.stage_01_parsing_raw_data import parse_txt
from src.cleaning_code_refactor_utils.find_RPF import find_RPF
from src.cleaning_code_refactor_utils.clean_fandom_labels import clean_fandoms
from src.cleaning_code_refactor_utils.clean_char_names import clean_names
from src.cleaning_code_refactor_utils.gather_chars_and_fandoms import gather_chars_and_fandoms

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

if __name__ == "__main__":
    parsed_dict = parse_txt()
    gathered_dict = gather_chars_and_fandoms(parsed_dict)
    cleaned_ranking_dict = clean_rankings(parsed_dict)
