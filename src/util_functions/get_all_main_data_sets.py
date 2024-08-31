from src.util_functions.get_file_paths import find_paths
from src.util_functions.retrieve_data_from_csv import read_data_from_csv
from src.util_functions.retrieve_data_from_json_lines import get_json_lines_data
from src.util_functions.get_data_set_name import get_data_set_name
from json import load

def get_all_main_sets(folder_path):
    """
    takes a folder path (as for find_paths) from which to retrieve all the main data sets 
    (stored in csv or json format)

    returns a dict with data set name keys and data set data values
    """

    all_paths = find_paths(folder_path) # returns list of filepaths

    all_data_sets = {}

    for path in all_paths:
        data_set = get_data_set_name(path)
        if path[-4:] == ".csv":
            # treat it as a csv
            loaded_data = read_data_from_csv(path)
        elif "json_lines" in folder_path:
            # treat it as json lines
            loaded_data = get_json_lines_data(path)
        elif path[-5:] == ".json":
            # treat it as a json
            with open(path, "r") as json_file:
                loaded_data = load(json_file)
        all_data_sets[data_set] = loaded_data
    
    return all_data_sets
