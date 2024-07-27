from src.second_cleaning_stage_code.unify_column_names import unify_column_names
from src.util_functions.get_file_paths import find_paths
from src.util_functions.retrieve_data_from_csv import read_data_from_csv
import pytest

@pytest.fixture
def all_file_paths():
    all_paths = find_paths("data/first_clean_up_data/")
    return all_paths

class TestUnifyColumnNames:
    def test_does_not_mutate_input_list(self):
        input_list = read_data_from_csv("data/first_clean_up_data/ao3_2015/raw_ao3_2015_femslash_ranking.csv")
            #using a file that would be affected by column name changes
        unify_column_names(input_list) 
        assert input_list == read_data_from_csv("data/first_clean_up_data/ao3_2015/raw_ao3_2015_femslash_ranking.csv")

    def test_returns_list_of_lists_of_same_length(self, all_file_paths):
        for path in all_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = unify_column_names(input_list)
            assert type(updated_list) == list
            assert len(updated_list) == len(input_list)
            for row in updated_list:
                assert type(row) == list
                assert len(row) == len(updated_list[0])

    def test_returns_updated_column_names(self, all_file_paths):
        for path in all_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = unify_column_names(input_list)
            column_names = [
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
            for column in updated_list[0]:
                assert column in column_names

    def test_returns_other_rows_unchanged(self, all_file_paths):
        for path in all_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = unify_column_names(input_list)
            for row in range(1, len(updated_list)):
                assert updated_list[row] == input_list[row]
