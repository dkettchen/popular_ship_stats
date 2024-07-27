from src.third_cleaning_stage_code.add_race_list_for_all_white_pairings import add_list_for_white_only_pairings
from src.util_functions.retrieve_data_from_csv import read_data_from_csv
from src.util_functions.get_file_paths import find_paths
import pytest

@pytest.fixture
def relevant_file_paths():
    all_paths = find_paths("data/second_clean_up_data/")
    relevant_paths = []
    for path in all_paths:
        if "2023" not in path \
        and "2022" not in path \
        and "2021" not in path \
        and "2013" not in path \
        and "2014_femslash" not in path \
        and "2015_femslash" not in path:
            relevant_paths.append(path)
    return relevant_paths


def test_does_not_mutate_input_list(relevant_file_paths):
    for path in relevant_file_paths:
        input_list = read_data_from_csv(path)
        add_list_for_white_only_pairings(input_list)
        assert input_list == read_data_from_csv(path)

def test_returns_list_of_lists_of_same_length(relevant_file_paths):
    for path in relevant_file_paths:
        input_list = read_data_from_csv(path)
        output_list = add_list_for_white_only_pairings(input_list)

        assert type(output_list) == list
        assert len(output_list) == len(input_list)
        for row in output_list:
            assert type(row) == list
            assert len(row) == len(input_list[0])

def test_returns_race_value_changed_to_list_for_white_white_pairings(relevant_file_paths):
    for path in relevant_file_paths:
        input_list = read_data_from_csv(path)
        output_list = add_list_for_white_only_pairings(input_list)
    
        for i in range(1, len(output_list)):
            row = output_list[i]
            old_row = input_list[i]

            if "2014" in path:
                column_index = -2
            else: 
                column_index = -1
            
            assert row[column_index] != "White"
            if old_row[column_index] == "White":
                assert type(row[column_index]) == list
                assert type(row[column_index][0]) == str and type(row[column_index][1]) == str
                assert row[column_index] == ["White", "White"]

def test_returns_other_race_values_unchanged(relevant_file_paths):
    for path in relevant_file_paths:
        input_list = read_data_from_csv(path)
        output_list = add_list_for_white_only_pairings(input_list)
        leftover_tags = [
            "Whi/POC", "POC", "Whi/Amb", "Ambig", "Amb/POC", "Amb/Whi", "POC/Whi", "POC/Amb"
            ]
    
        for i in range(1, len(output_list)):
            row = output_list[i]
            old_row = input_list[i]

            if "2014" in path:
                column_index = -2
            else: 
                column_index = -1
            
            if old_row[column_index] != "White":
                assert row[column_index] != ["White", "White"]
                assert type(row[column_index]) == str
                assert row[column_index] in leftover_tags

def test_returns_remaining_values_unchanged(relevant_file_paths):
    for path in relevant_file_paths:
        input_list = read_data_from_csv(path)
        output_list = add_list_for_white_only_pairings(input_list)

        assert output_list[0] == input_list[0]
        for i in range(1, len(output_list)):
            row = output_list[i]
            old_row = input_list[i]

            if "2014" in path:
                column_index = -2
            else: 
                column_index = -1
            
            for index in range(len(row)):
                if index != len(row) + column_index: 
                            # cause we counted from the back rather than the front
                    assert row[index] == old_row[index]

