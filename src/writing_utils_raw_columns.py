from json import dump
from split_values import split_raw_data_2013_2014_and_2020_to_2023, split_raw_data_2015_to_2019
from get_file_paths import find_paths

def get_all_column_names():
    """
    extracts column names from all raw_data sets

    returns a dict with keys named after the data set and a list of the corresponding column names
    """
    #get file paths
    all_paths = find_paths("data/raw_data/")

    output_dict = {}

    for path in all_paths:
    #run split functions on all data sets
        if "2013_overall_ranking" in path \
        or "2014" in path \
        or "202" in path: # all relevant 2013, 2014, and 2020-2023 data sets
            split_list = split_raw_data_2013_2014_and_2020_to_2023(path)
        elif "2015" in path \
        or "2016" in path \
        or "2017" in path \
        or "2019" in path: # all 2015-2019 data sets
            split_list = split_raw_data_2015_to_2019(path)
        else: continue #pesky 2013 non-ranking files need to be stopped smh

    #copy first row into a dict w data set names as keys
        if not split_list[0][-1] == "":
            output_dict[path[27:-4]] = split_list[0]
        else: output_dict[path[27:-4]] = split_list[0][:-1]

    keys = list(output_dict.keys())
    keys.sort()
    sorted_dict = {i: output_dict[i] for i in keys}

    with open("data/reference_and_test_files/all_data_set_column_names.json", "w") as column_file:
        dump(sorted_dict, column_file, indent=4)

