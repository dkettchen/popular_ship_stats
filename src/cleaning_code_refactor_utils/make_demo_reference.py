from src.cleaning_code_refactor_utils.gathered_data_to_df import gathered_data_to_df
from src.cleaning_code_refactor.stage_03_adding_demo_data import (
    gather_char_demo_data, 
    gather_ship_demo_data, 
)
from data.reference_and_test_files.refactor_helper_files.folder_lookup import TOTAL_DATA_FOLDER

def make_demo_reference(cleaned_ranking_dict:dict):
    """
    takes a dict of dicts of dfs with cleaned fandom and character names

    creates reference csv files for fandoms, characters & ships
    with demo data & things like canon status included in the latter two
    """

    # get demo data for each char
    gathered_demo_data = gather_char_demo_data(cleaned_ranking_dict)
    # get demo data for each ship
    gathered_ship_data = gather_ship_demo_data(cleaned_ranking_dict, gathered_demo_data)
    # print reference csvs
    for case in ["fandoms", "characters", "ships"]:
        if case == "ships":
            gathered_data = gathered_ship_data
        else:
            gathered_data = gathered_demo_data
        df = gathered_data_to_df(gathered_data, case)
        df.to_csv(f"{TOTAL_DATA_FOLDER}/{case[:-1]}_data.csv") # prints reference csv files
