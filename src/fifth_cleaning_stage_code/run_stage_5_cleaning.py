#TODO:
# data set table: ✅
# - go through (sorted?) list of filepaths ✅
# - collect:
    # - year ✅
    # - type ✅
# - set website to be "AO3" for all these ones ✅
# possibly convert to a csv file instead of json due to no collection values or anything? ✅
    # use util ✅

# characters table: ✅
    # (they all have their fandom in their dicts, so don't need to be classified by those)
    # - un-categorise them -> we want a list of char names (as keys w dict values) ✅
    # - add rpf or fic value ✅
# - if we extract & save op versions in a separate file we can save this as a csv o.o ✅
    # - extract op versions & save separately under same key names! ✅
    # -> make old names csv ✅

# pairings table:
    # - key of alphabetically sorted ship member names (to reuse in main sets later)
    # - members of pairing (make into individual rows?)
    # - num of members in pairing
    # - gender info (either combo and/or per member?)
    # - race info (either combo, whether it's interracial or no, and/or per member?)

# main sets:
# -> add pairing strings (same as keys from pairings table)
# - remove gender from type column - replace with gen or slash only
# - remove race column
# - make rank a simple number
    # possibly add a "tied" column???
# - make change a simple value (ie pos. num, neg. num, "new", none)
# - add data set column


# this file should be the one running the functions & creating all the files in question
# rather than each file its own files
# -> so we only have to run this file

from json import dump
from src.fifth_cleaning_stage_code.make_character_table import make_sorted_char_dict, prep_characters_for_csv
from src.fifth_cleaning_stage_code.make_old_names_table import make_old_names_dict, prep_old_names_for_csv
from src.util_functions.write_csv_file import make_csv_file
from src.util_functions.get_all_main_data_sets import get_all_main_sets
from src.fifth_cleaning_stage_code.make_main_tables import make_ranking_table
from src.fifth_cleaning_stage_code.make_pairing_table import make_ships_dict


if __name__ == "__main__":
    sorted_char_dict = make_sorted_char_dict()
    json_chars_filepath = "data/fifth_clean_up_data/stage_5_characters.json"
    with open(json_chars_filepath, "w") as char_file:
        dump(sorted_char_dict, char_file, indent=4)
    
    csv_char_list = prep_characters_for_csv(sorted_char_dict)
    csv_chars_filepath = "data/fifth_clean_up_data/stage_5_characters.csv"
    make_csv_file(csv_char_list, csv_chars_filepath)

    old_dict = make_old_names_dict(sorted_char_dict)
    prepped_old_names = prep_old_names_for_csv(old_dict)
    csv_old_names_filepath = "data/fifth_clean_up_data/stage_5_old_names.csv"
    make_csv_file(prepped_old_names, csv_old_names_filepath)

    all_main_data_sets = get_all_main_sets("data/fourth_clean_up_data/")
    ship_dict = make_ships_dict(all_main_data_sets)
    json_ships_filepath = "data/fifth_clean_up_data/stage_5_ships.json"
    with open(json_ships_filepath, "w") as json_ship_file:
        dump(ship_dict, json_ship_file, indent=4)

    # for data_set_name in all_main_data_sets:
    #     data = all_main_data_sets[data_set_name]
    #     ranking = make_ranking_table(data, data_set_name)