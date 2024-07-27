from src.second_cleaning_stage_code.clean_all_number_values import (
    remove_commas_from_2015_2016_fics_tallies, 
    separate_ranking_equals,
    separate_change_symbols
)
from src.util_functions.retrieve_data_from_csv import read_data_from_csv
from src.util_functions.get_file_paths import find_paths
import pytest

@pytest.fixture
def relevant_2015_16_file_paths():
    return [
        "data/first_clean_up_data/ao3_2015/raw_ao3_2015_femslash_ranking.csv",
        "data/first_clean_up_data/ao3_2015/raw_ao3_2015_overall_ranking.csv",
        "data/first_clean_up_data/ao3_2016/raw_ao3_2016_femslash_ranking.csv",
        "data/first_clean_up_data/ao3_2016/raw_ao3_2016_overall_ranking.csv",
        "data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv"
    ]

@pytest.fixture
def all_file_paths():
    all_paths = find_paths("data/first_clean_up_data/")
    return all_paths

@pytest.fixture
def change_file_paths(all_file_paths):
    relevant_paths = []
    for path in all_file_paths:
        if "2013" not in path and "2014_femslash" not in path and "2016_data" not in path:
            relevant_paths.append(path)
    return relevant_paths


class TestRemoveCommas:
    def test_commas_does_not_mutate_input_list(self):
        input_list = read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")
        remove_commas_from_2015_2016_fics_tallies(input_list)
        assert input_list == read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")

    def test_commas_returns_list_of_lists_of_same_length(self, relevant_2015_16_file_paths):
        for path in relevant_2015_16_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = remove_commas_from_2015_2016_fics_tallies(input_list)
            assert type(updated_list) == list
            assert len(updated_list) == len(input_list)
            for row in updated_list:
                assert type(row) == list
                assert len(row) == len(updated_list[0])

    def test_commas_returns_works_columns_turned_into_ints(self, relevant_2015_16_file_paths):
        for path in relevant_2015_16_file_paths:
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

    def test_commas_returns_other_values_unchanged(self, relevant_2015_16_file_paths):
        for path in relevant_2015_16_file_paths:
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
    def test_ranks_does_not_mutate_input_list(self):
        input_list = read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")
        separate_ranking_equals(input_list)
        assert input_list == read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")

    def test_ranks_returns_list_of_lists_of_same_length(self, all_file_paths):
        for path in all_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = separate_ranking_equals(input_list)
            assert type(updated_list) == list
            assert len(updated_list) == len(input_list)
            for row in updated_list:
                assert type(row) == list
                assert len(row) == len(updated_list[0])

    def test_ranks_returns_a_ranking_value_with_an_int_and_none_or_equal_sign_item(self, all_file_paths):
        for path in all_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = separate_ranking_equals(input_list)
            for column in range(len(updated_list[0])):
                if updated_list[0][column] == "#" or updated_list[0][column] == "Rank":
                    index = column
            for row in updated_list[1:]:
                assert type(row[index]) == list
                assert type(row[index][0]) == int
                assert row[index][1] == None or row[index][1] == "="

    def test_ranks_returns_other_values_unchanged(self, all_file_paths):
        for path in all_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = separate_ranking_equals(input_list)
            if "2014_overall" in path:
                indexes = [0, 2, 3, 4, 5, 6]
                for row in range(len(updated_list[1:])):
                    for index in indexes:
                        assert updated_list[row][index] == input_list[row][index]
            else: 
                for row in range(len(updated_list[1:])):
                    for index in range(1, len(updated_list[row])):
                        assert updated_list[row][index] == input_list[row][index]

class TestSeparateRankingChange:
    def test_change_does_not_mutate_input_list(self):
        input_list = read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_femslash_ranking.csv")
        separate_change_symbols(input_list)
        assert input_list == read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_femslash_ranking.csv")

    def test_change_returns_list_of_lists_of_same_length(self, change_file_paths):
        for path in change_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = separate_change_symbols(input_list)
            assert type(updated_list) == list
            assert len(updated_list) == len(input_list)
            for row in updated_list:
                assert type(row) == list
                assert len(row) == len(updated_list[0])

    def test_change_returns_first_value_as_rank_and_second_value_as_change(self, change_file_paths):
        for path in change_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = separate_change_symbols(input_list)
            assert updated_list[0][0] == "Rank" or updated_list[0][0] == "#"
            assert updated_list[0][1] == "Change" or updated_list[0][1] == "New"
            for row in updated_list[1:]:
                change = row[1]
                assert type(change) == list

    def test_change_returns_a_ranking_value_with_expected_values(self, change_file_paths):
        for path in change_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = separate_change_symbols(input_list)
            for row in updated_list[1:]:
                change = row[1]
                assert change[0] in ["+", "-", "New"] or change[0] == None
                assert type(change[1]) == int or change[1] == None
                if change[0] == "New":
                    assert change == ["New", None]
                elif change[0] in ["+", "-"]:
                    assert type(change[1]) == int
                elif not change[0]: # if change is none
                    assert not change[1] #must be 0 or none

    def test_change_returns_other_values_unchanged(self, change_file_paths):
        for path in change_file_paths:
            input_list = read_data_from_csv(path)
            updated_list = separate_change_symbols(input_list)
            for row in range(len(updated_list)):
                if "2014_overall" not in path:
                    assert updated_list[row][0] == input_list[row][0]
                else: 
                    assert updated_list[row][0] == input_list[row][1]
                for index in range(2, len(updated_list[row])):
                    assert updated_list[row][index] == input_list[row][index]

