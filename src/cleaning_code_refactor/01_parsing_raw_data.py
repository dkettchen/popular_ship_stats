from src.cleaning_code_refactor_utils.find_paths import find_paths
from src.cleaning_code_refactor_utils.read_txt import read_txt
from src.cleaning_code_refactor_utils.split_values import split_data, split_data_2015_to_2019

files = find_paths("data/raw_data")

filepaths = {
    # 2013, 2014
    "early_paths" : [path for path in files if "2014" in path or "2013_overall" in path],
    # 2015-2019
    "middle_paths" : [path for path in files if "201" in path and "2013" not in path and "2014" not in path],
    # 2020-present
    "recent_paths" : [path for path in files if "202" in path]
}

for group in filepaths:
    for filepath in filepaths[group]: # going through all files

        # read in data
        read_data = read_txt(filepath)

        # retrieving year & ranking from filepath
        year = int(filepath[31:35])
        ranking = filepath[36:-4]
        if "ranking" in ranking:
            ranking = ranking[:-8]
        if "2019_" in ranking:
            ranking = ranking[5:]

        if year not in [2015, 2016, 2017, 2019]:
            split_list = split_data(read_data, year, ranking)
        else:
            split_list = split_data_2015_to_2019(read_data, year, ranking)


    # new_list = separate_pairings(old_list)
    # file_path = "data/first_clean_up_data/" + path[14:-4] + ".csv"
    # final_list = escape_apostrophes(new_list)
    # make_csv_file(final_list, file_path)

# for path in early_paths:

#     new_list1 = separate_pairings(old_list1)
#     file_path1 = "data/first_clean_up_data/" + path[14:-4] + ".csv"
#     final_list1 = escape_apostrophes(new_list1)
#     make_csv_file(final_list1, file_path1)

# for path in middle_paths:

#     old_list2 = split_pairings_from_fandoms(old_list_unseparated)
#     new_list2 = separate_pairings(old_list2)
#     file_path2 = "data/first_clean_up_data/" + path[14:-4] + ".csv"
#     final_list2 = escape_apostrophes(new_list2)
#     make_csv_file(final_list2, file_path2)