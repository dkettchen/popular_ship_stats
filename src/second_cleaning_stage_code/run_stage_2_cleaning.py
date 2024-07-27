from src.util_functions.get_file_paths import find_paths
from src.util_functions.retrieve_data_from_csv import read_data_from_csv
from src.second_cleaning_stage_code.clean_all_number_values import (
    remove_commas_from_2015_2016_fics_tallies, 
    separate_ranking_equals, 
    separate_change_symbols
)
from src.second_cleaning_stage_code.unify_column_names import unify_column_names
from src.util_functions.write_csv_file import make_csv_file

def run_cleaning_stage_2():
    all_paths = find_paths("data/first_clean_up_data/")
    for path in all_paths:
        input_list = read_data_from_csv(path)
        if "2015" in path or "2016" in path:
            input_list = remove_commas_from_2015_2016_fics_tallies(input_list)
        separated_rankings = separate_ranking_equals(input_list)
        if "2013" not in path and "2014_femslash" not in path and "2016_data" not in path:
            separated_change = separate_change_symbols(separated_rankings)
            final_list = unify_column_names(separated_change)
        else:
            final_list = unify_column_names(separated_rankings)
        file_path = "data/second_clean_up_data/" + path[25:-4] + ".csv"

        make_csv_file(final_list, file_path)

if __name__ == "__main__":
    run_cleaning_stage_2()
    pass
