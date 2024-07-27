from src.util_functions.get_file_paths import find_paths
from src.util_functions.retrieve_data_from_csv import read_data_from_csv
from src.second_cleaning_stage_code.clean_all_number_values import (
    remove_commas_from_2015_2016_fics_tallies, 
    separate_ranking_equals, 
    separate_change_symbols
)
from src.second_cleaning_stage_code.unify_column_names import unify_column_names
import pytest

@pytest.fixture
def all_file_paths():
    all_paths = find_paths("data/first_clean_up_data/")
    return all_paths

@pytest.fixture
def all_formatted_data(all_file_paths):
    """
    returns a list of dicts containing the path (on "path" key) 
    and formatted list (on "data" key) for each data set in all_file_paths
    """
    all_data_sets = []
    for path in all_file_paths:
        input_list = read_data_from_csv(path)
        if "2015" in path or "2016" in path:
            input_list = remove_commas_from_2015_2016_fics_tallies(input_list)
        separated_rankings = separate_ranking_equals(input_list)
        if "2013" not in path and "2014_femslash" not in path and "2016_data" not in path:
            separated_change = separate_change_symbols(separated_rankings)
            final_list = unify_column_names(separated_change)
        else:
            final_list = unify_column_names(separated_rankings)
        all_data_sets.append({"path": path, "data": final_list})
    return all_data_sets


class TestFinalTests:
    def test_all_column_names_are_expected_names(self, all_formatted_data):
        for data_dict in all_formatted_data:
            final_list = data_dict["data"]
            path = data_dict["path"]

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
            for column in final_list[0]:
                assert column in column_names #assert all columns are in correct column names

    def test_first_columns_is_rank(self, all_formatted_data):
        for data_dict in all_formatted_data:
            final_list = data_dict["data"]
            path = data_dict["path"]

            assert final_list[0][0] == "Rank" # assert that first column is "Rank"
            #assert each rank column value is a list, with the correct format:
            for row in final_list[1:]:
                assert type(row[0]) == list
                assert type(row[0][0]) == int
                assert row[0][1] in [None, "="]

    def test_second_column_is_change_where_change_is_present(self, all_formatted_data):
        for data_dict in all_formatted_data:
            final_list = data_dict["data"]
            path = data_dict["path"]

            if "2013" not in path and "2014_femslash" not in path and "2016_data" not in path: 
                    #if there is a change value 
                assert "Change" in final_list[0]
                assert final_list[0][1] == "Change" # assert that second column is "Change"
                # assert that every value in change column is list with correct format:
                for row in final_list[1:]:
                    assert type(row[1]) == list
                    assert row[1] in [[None, 0], ["New", None], [None, None]
                    ] or (row[1][0] in ["+", "-"] and type(row[1][1]) == int)

    def test_total_works_is_an_int(self, all_formatted_data):
        for data_dict in all_formatted_data:
            final_list = data_dict["data"]
            path = data_dict["path"]
            for column in range(len(final_list[0])):
                if final_list[0][column] == "Total Works": # locate index
                    index = column
            for row in final_list[1:]:
                assert type(row[index]) == int # assert all values in it are ints

    def test_new_works_where_present_is_an_int(self, all_formatted_data):
        for data_dict in all_formatted_data:
            final_list = data_dict["data"]
            path = data_dict["path"]

            if "data.csv" in path and "2016" not in path: #if new works column
                assert "New Works" in final_list[0]
                for column in range(len(final_list[0])):
                    if final_list[0][column] == "New Works": # locate index
                        index = column
                for row in final_list[1:]:
                    assert type(row[index]) == int # assert all values in it are ints
    
    def test_returns_row_and_list_length_unchanged(self, all_formatted_data):
        for data_dict in all_formatted_data:
            final_list = data_dict["data"]
            path = data_dict["path"]
            input_list = read_data_from_csv(path)

            assert len(final_list) == len(input_list)
            for i in range(len(final_list)):
                assert len(final_list[i]) == len(input_list[i])

    def test_returns_remaining_values_unchanged(self, all_formatted_data):
        for data_dict in all_formatted_data:
            final_list = data_dict["data"]
            path = data_dict["path"]
            input_list = read_data_from_csv(path)

            rank_index = 0
            change_index = None
            new_works_index = None
            if "2013" not in path and "2014_femslash" not in path and "2016_data" not in path: 
                change_index = 1
            for column in range(len(final_list[0])):
                if final_list[0][column] == "Total Works":
                    total_index = column
            if "data.csv" in path:
                for column1 in range(len(final_list[0])):
                    if final_list[0][column1] == "New Works":
                        new_works_index = column1

            formatted_indexes = [rank_index, change_index, total_index, new_works_index]

            for i in range(len(final_list[0])):
                if i not in formatted_indexes: # if it's a non-formatted column
                    for row in range(1, len(final_list)):
                        print(total_index, path)
                        assert final_list[row][i] == input_list[row][i]

            
            


            #we've formatted the first column, the change column, the 