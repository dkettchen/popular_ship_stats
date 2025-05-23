from src.cleaning_code_refactor.stage_01_parsing_raw_data import parse_txt
import pandas as pd
from src.cleaning_code_refactor_utils.gather_chars_and_fandoms import gather_raw_chars_and_fandoms
from src.cleaning_code_refactor_utils.find_RPF import find_RPF
from src.cleaning_code_refactor_utils.clean_fandom_labels import clean_fandoms
from src.cleaning_code_refactor_utils.clean_char_names import clean_names
from json import dump

def clean_names(parsed_dict:dict):
    ## fourth stage cleaning 

    # collecting all raw fandom & char names
    raw_fandoms_and_chars = gather_raw_chars_and_fandoms(parsed_dict)

    ## fandoms

    # extracting fandoms
    fandom_df = pd.DataFrame(sorted(list(raw_fandoms_and_chars.keys())), columns=["Fandom"])
    fandom_df = find_RPF(fandom_df) # adding RPF bool column

    # cleaning fandoms & sort alphabetically
    fandom_df["New Fandom"] = fandom_df["Fandom"].apply(clean_fandoms)
    fandom_df = fandom_df.rename(columns={
        "Fandom": "Old Fandom", 
        "New Fandom": "Fandom"
    }).set_index("Old Fandom").sort_values("Fandom")

    # print all fandoms to a list to look at em (currently all fandoms up to 2024 are parsed correctly)
    all_fandoms = list(fandom_df["Fandom"].unique())
    with open("data/reference_and_test_files/refactor_helper_files/fandoms.json", "w") as fandoms_json:
        dump(all_fandoms, fandoms_json, indent=4)

    # combine characters per new fandom
    new_fandoms_and_chars = {fandom: set() for fandom in all_fandoms}
    for old_fandom in fandom_df.index:
        new_fandom = fandom_df["Fandom"].loc[old_fandom]
        characters = raw_fandoms_and_chars[old_fandom]
        for char in characters:
            new_fandoms_and_chars[new_fandom].add(char)
    for key in new_fandoms_and_chars:
        new_fandoms_and_chars[key] = sorted(list(new_fandoms_and_chars[key]))

    ## characters

    # make a char name df
    char_names = []
    for fandom in new_fandoms_and_chars:
        for char in new_fandoms_and_chars[fandom]:
            char_dict = {
                "Old Name": char,
                "Fandom": fandom
            }
            char_names.append(char_dict)
    char_df = pd.DataFrame(char_names)

    # clean names
    char_df["New Name"] = char_df["Old Name"].apply(clean_names)








if __name__ == "__main__":
    parsed_dict = parse_txt()
    clean_names(parsed_dict)



    # for later:

    # generate filepath

    # generate folders along with files
    # print to csv files with ` as escape char
