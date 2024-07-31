from src.third_cleaning_stage_code.add_race_list_for_all_white_pairings import add_list_for_white_only_pairings
from src.third_cleaning_stage_code.add_missing_columns import add_missing_columns
from src.third_cleaning_stage_code.run_third_stage_cleaning import turning_apostrophes_back
from src.util_functions.get_file_paths import find_paths
from src.util_functions.retrieve_data_from_csv import read_data_from_csv
import pytest

@pytest.fixture
def all_read_data():
    """
    returns a list of dicts containing the relevant path on a "path" key
    and the data read from the corresponding 2nd stage csv file
    on a "csv_data" key
    """
    all_paths = find_paths("data/second_clean_up_data/")
    all_data_sets = []
    for path in all_paths:
        input_list = read_data_from_csv(path)
        output_dict = {
            "path" : path, "csv_data" : input_list
        }
        all_data_sets.append(output_dict)
    return all_data_sets

@pytest.fixture
def all_formatted_data_sets(all_read_data):
    """
    returns a list of dicts containing the relevant path on a "path" key
    and the corresponding formatted data on a "formatted_data" key
    """
    all_data_sets = []
    for data_set in all_read_data:
        path = data_set["path"]
        input_list = data_set["csv_data"]
        added_white_lists = add_list_for_white_only_pairings(input_list)
        added_columns = add_missing_columns(added_white_lists)
        data = turning_apostrophes_back(added_columns)
        output_dict = {
            "path" : path, "formatted_data" : data
        }
        all_data_sets.append(output_dict)
    return all_data_sets


class TestFormatting:
    def test_returns_list_of_dicts_of_same_length_as_original_data_set(self, all_formatted_data_sets, all_read_data):
        for index in range(len(all_formatted_data_sets)):
            path = all_formatted_data_sets[index]["path"]
            input_list = all_read_data[index]["csv_data"]
            output_list = all_formatted_data_sets[index]["formatted_data"]

            assert len(output_list) == len(input_list) - 1
            assert type(output_list) == list
            for item in output_list:
                assert type(item) == dict
    
    def test_returns_dicts_of_9_keys(self, all_formatted_data_sets):
        for data_set in all_formatted_data_sets:
            path = data_set["path"]
            formatted_list = data_set["formatted_data"]

            for item in formatted_list:
                assert len(item) == 9
    
    def test_returns_dicts_of_expected_keys_with_expected_value_types(self, all_formatted_data_sets):
        for data_set in all_formatted_data_sets:
            path = data_set["path"]
            formatted_list = data_set["formatted_data"]

            for item in formatted_list:
                assert list(item.keys()) == [
                    "Rank", 
                    "Change", 
                    "Relationship", 
                    "Fandom", 
                    "New Works", 
                    "Total Works", 
                    "Type", 
                    "Race", 
                    "Release Date"
                ]
                
                assert type(item["Rank"]) == list
                assert type(item["Rank"][0]) == int
                assert type(item["Change"]) == list
                assert type(item["Relationship"]) == list
                for character in item["Relationship"]:
                    assert type(character) == str
                assert type(item["Fandom"]) == str
                assert type(item["New Works"]) == int or item["New Works"] == None
                assert type(item["Total Works"]) == int
                assert type(item["Type"]) == list or type(item["Type"]) == str
                assert type(item["Race"]) == list or type(item["Race"]) == str
                assert type(item["Release Date"]) == str or item["Release Date"] == None

    def test_no_longer_contains_White_strings(self, all_formatted_data_sets):
        for data_set in all_formatted_data_sets:
            path = data_set["path"]
            formatted_list = data_set["formatted_data"]

            for item in formatted_list:
                assert item["Race"] != "White"

    def test_no_longer_contains_double_quotes(self, all_formatted_data_sets):
        for data_set in all_formatted_data_sets:
            path = data_set["path"]
            formatted_list = data_set["formatted_data"]

            for item in formatted_list:
                assert '"' not in item["Fandom"]
                for character in item["Relationship"]:
                    assert '"' not in character