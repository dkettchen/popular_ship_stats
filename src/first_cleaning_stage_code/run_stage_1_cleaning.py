from src.util_functions.get_file_paths import find_paths
from src.first_cleaning_stage_code.split_values import split_raw_data_2013_2014_and_2020_to_2023, split_raw_data_2015_to_2019, split_pairings_from_fandoms
from src.first_cleaning_stage_code.separate_values import separate_pairings
from src.util_functions.write_csv_file import make_csv_file

def run_cleaning_stage_1():
    """
    runs all code necessary to 
    clean raw ao3 txt files in data/raw_data/, 
    and write the cleaned data into csv files in data/first_clean_up_data/
    """

    all_raw_data = find_paths("data/raw_data/")
    early_paths = [
        path for path in all_raw_data \
        if "2013_overall" in path \
        or "2014" in path
            ]
    middle_paths = [
        path for path in all_raw_data \
        if "2015" in path \
        or "2016" in path \
        or "2017" in path \
        or "2019" in path
            ]
    recent_paths = [path for path in all_raw_data if "202" in path]

    for path in recent_paths:
        old_list = split_raw_data_2013_2014_and_2020_to_2023(path)
        new_list = separate_pairings(old_list)
        file_path = "data/first_clean_up_data/" + path[14:-4] + ".csv"
        make_csv_file(new_list, file_path)

    for path in early_paths:
        old_list1 = split_raw_data_2013_2014_and_2020_to_2023(path)
        new_list1 = separate_pairings(old_list1)
        file_path1 = "data/first_clean_up_data/" + path[14:-4] + ".csv"
        make_csv_file(new_list1, file_path1)

    for path in middle_paths:
        old_list_unseparated = split_raw_data_2015_to_2019(path)
        old_list2 = split_pairings_from_fandoms(old_list_unseparated)
        new_list2 = separate_pairings(old_list2)
        file_path2 = "data/first_clean_up_data/" + path[14:-4] + ".csv"
        make_csv_file(new_list2, file_path2)


if __name__ == "__main__":
    run_cleaning_stage_1()
    pass