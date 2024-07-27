from src.second_cleaning_stage_code.clean_all_number_values import (
    remove_commas_from_2015_2016_fics_tallies, 
    separate_ranking_equals,
    separate_change_symbols
)
from src.util_functions.retrieve_data_from_csv import read_data_from_csv
import pytest

@pytest.fixture
def relevant_file_paths():
    return [
        "data/first_clean_up_data/ao3_2015/raw_ao3_2015_femslash_ranking.csv",
        "data/first_clean_up_data/ao3_2015/raw_ao3_2015_overall_ranking.csv",
        "data/first_clean_up_data/ao3_2016/raw_ao3_2016_femslash_ranking.csv",
        "data/first_clean_up_data/ao3_2016/raw_ao3_2016_overall_ranking.csv",
        "data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv"
    ]

class TestRemoveCommas:
    def test_does_not_mutate_input_list(self):
        input_list = read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")
        remove_commas_from_2015_2016_fics_tallies(input_list)
        assert input_list == read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")

    def test_returns_list_of_lists_of_same_length(self, relevant_file_paths):
        for path in relevant_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = remove_commas_from_2015_2016_fics_tallies(input_list)
            assert type(updated_list) == list
            assert len(updated_list) == len(input_list)
            for row in updated_list:
                assert type(row) == list
                assert len(row) == len(updated_list[0])

    def test_returns_works_columns_turned_into_ints(self, relevant_file_paths):
        for path in relevant_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = remove_commas_from_2015_2016_fics_tallies(input_list)
            for row in updated_list[1:]:
                if "2016_data" in path:
                    assert type(row[-3]) == int
                    assert type(row[-4]) == int
                elif "femslash" in path:
                    print(row)
                    assert type(row[-2]) == int
                elif "overall" in path:
                    assert type(row[-3]) == int

    def test_returns_other_values_unchanged(self, relevant_file_paths):
        for path in relevant_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = remove_commas_from_2015_2016_fics_tallies(input_list)
            for row in range(len(updated_list[1:])):
                if "2016_data" in path:
                    indexes = [0, 1, 2, 5, 6]
                    for index in indexes:
                        assert updated_list[row][index] == input_list[row][index]
                elif "femslash" in path:
                    indexes = [0, 1, 2, 3, 5]
                    for index in indexes:
                        assert updated_list[row][index] == input_list[row][index]
                elif "overall" in path:
                    indexes = [0, 1, 2, 3, 5, 6]
                    for index in indexes:
                        assert updated_list[row][index] == input_list[row][index]

class TestSeparateRankingEquals:
    def test_does_not_mutate_input_list(self):
        input_list = read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")
        separate_ranking_equals(input_list)
        assert input_list == read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")

    def test_returns_list_of_lists_of_same_length(self, relevant_file_paths):
        for path in relevant_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = separate_ranking_equals(input_list)
            assert type(updated_list) == list
            assert len(updated_list) == len(input_list)
            for row in updated_list:
                assert type(row) == list
                assert len(row) == len(updated_list[0])

    def test_returns_a_list_value_with_an_int_and_none_or_equal_sign_item(self, relevant_file_paths):
        for path in relevant_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = separate_ranking_equals(input_list)
            for row in updated_list[1:]:
                assert type(row[0][0]) == int
                assert row[0][1] == None or row[0][1] == "="

    def test_returns_other_values_unchanged(self, relevant_file_paths):
        for path in relevant_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = separate_ranking_equals(input_list)
            for row in range(len(updated_list[1:])):
                for index in range(1, len(updated_list[row])):
                    assert updated_list[row][index] == input_list[row][index]
