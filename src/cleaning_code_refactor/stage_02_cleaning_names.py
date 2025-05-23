from src.cleaning_code_refactor.stage_01_parsing_raw_data import parse_txt
import pandas as pd
from src.cleaning_code_refactor_utils.gather_chars_and_fandoms import gather_raw_chars_and_fandoms
from src.cleaning_code_refactor_utils.find_RPF import find_RPF
from src.cleaning_code_refactor_utils.clean_fandom_labels import clean_fandoms
from json import dump

def clean_names(parsed_dict:dict):
    ## fourth stage cleaning 

    # collecting names
    raw_fandoms_and_chars = gather_raw_chars_and_fandoms(parsed_dict)

    # TODO
            # reference unify fandoms file
        # clean fandoms
        # then make a fandom df w new names, old names & indexes


            # return to referencing separate names into parts file
        # combine characters per new bigger fandoms
        # clean characters

    # extracting fandoms
    fandom_df = pd.DataFrame(sorted(list(raw_fandoms_and_chars.keys())), columns=["Fandom"])
    fandom_df = find_RPF(fandom_df) # adding RPF bool column

    # cleaning fandoms
    fandom_df["New Fandom"] = fandom_df["Fandom"].apply(clean_fandoms)
    fandom_df = fandom_df.rename(columns={
        "Fandom": "Old Fandom", 
        "New Fandom": "Fandom"
    }).sort_values("Fandom")

    all_fandoms = list(fandom_df["Fandom"].unique())
    with open("data/reference_and_test_files/refactor_helper_files/fandoms.json", "w") as fandoms_json:
        dump(all_fandoms, fandoms_json, indent=4)


    # later we still need to order the fandoms alphabetically







if __name__ == "__main__":
    parsed_dict = parse_txt()
    clean_names(parsed_dict)



    # for later:

    # generate filepath

    # generate folders along with files
    # print to csv files with ` as escape char
