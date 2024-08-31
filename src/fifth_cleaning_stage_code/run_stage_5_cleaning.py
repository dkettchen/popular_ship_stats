from json import dump
from src.fifth_cleaning_stage_code.make_character_table import make_sorted_char_dict, prep_characters_for_csv
from src.fifth_cleaning_stage_code.make_old_names_table import make_old_names_dict, prep_old_names_for_csv
from src.util_functions.write_csv_file import make_csv_file
from src.util_functions.get_all_main_data_sets import get_all_main_sets
from src.fifth_cleaning_stage_code.make_main_tables import make_ranking_table
from src.fifth_cleaning_stage_code.make_pairing_table import make_ships_dict, prep_ships_for_csv


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

    ship_list = prep_ships_for_csv(ship_dict)
    csv_ship_filepath = "data/fifth_clean_up_data/stage_5_ships.csv"
    make_csv_file(ship_list, csv_ship_filepath)

    for data_set_name in all_main_data_sets:
        data = all_main_data_sets[data_set_name]
        ranking = make_ranking_table(data, data_set_name)
        ranking_filepath = f'data/fifth_clean_up_data/{data_set_name[:8].lower()}/stage_5_{data_set_name.lower()}.csv'
        make_csv_file(ranking, ranking_filepath)