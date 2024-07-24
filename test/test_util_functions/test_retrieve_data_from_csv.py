from src.util_functions.retrieve_data_from_csv import read_data_from_csv
from src.util_functions.get_file_paths import find_paths

class TestCSVReader:
    def test_returns_list_of_lists(self):
        all_paths = find_paths("data/first_clean_up_data/")
        for path in all_paths:
            data_list = read_data_from_csv(path)
            assert type(data_list) == list
    
