from src.third_cleaning_stage_code.add_missing_columns import add_missing_columns
from src.util_functions.retrieve_data_from_csv import read_data_from_csv
from src.util_functions.get_file_paths import find_paths
import pytest

@pytest.fixture
def all_file_paths():
    all_paths = find_paths("data/second_clean_up_data/")
    return all_paths


def test_does_not_mutate_input_list(all_file_paths):
    for path in all_file_paths:
        input_list = read_data_from_csv(path)
        add_missing_columns(input_list)
        assert input_list == read_data_from_csv(path)

def test_returns_list_of_dicts_of_same_length_minus_header_row(all_file_paths):
    for path in all_file_paths:
        input_list = read_data_from_csv(path)
        output_list = add_missing_columns(input_list)

        assert type(output_list) == list
        assert len(output_list) == len(input_list) - 1
        for row in output_list:
            assert type(row) == dict

def test_returns_dicts_with_expected_keys(all_file_paths):
    for path in all_file_paths:
        input_list = read_data_from_csv(path)
        output_list = add_missing_columns(input_list)

        for row in output_list:
            assert len(row) == 9
            assert list(row.keys()) == [
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

def test_returns_expected_key_value_pairs(all_file_paths):
    for path in all_file_paths:
        input_list = read_data_from_csv(path)
        output_list = add_missing_columns(input_list)

        for row in output_list:
            assert type(row["Rank"]) == list
            assert len(row["Rank"]) == 2
            assert type(row["Rank"][0]) == int
            assert row["Rank"][1] == None or row["Rank"][1] == "="

            assert type(row["Change"]) == list
            assert len(row["Change"]) == 2
            assert row["Change"][0] == None or row["Change"][0] in ["+", "-", "New"]
            assert row["Change"][1] == None or type(row["Change"][1]) == int
        
            assert type(row["Relationship"]) == list
            assert len(row["Relationship"]) >= 2
            for character in row["Relationship"]:
                assert type(character) == str
            
            assert type(row["Fandom"]) == str
            assert type(row["New Works"]) == int or row["New Works"] == None
            assert type(row["Total Works"]) == int

            assert type(row["Type"]) == list or type(row["Type"]) == str
            if type(row["Type"]) == list:
                assert len(row["Type"]) == 2
                assert row["Type"] in [["M","M"], ["F","F"], ["F","M"]]
            elif type(row["Type"]) == str:
                assert row["Type"] in ["Other", "Gen", "Poly"]

            racial_groups = [
                "White", 
                "Asian", 
                "Latino", 
                "MENA", 
                "Black", 
                "Af Lat",
                "Indig", 
                "Ambig", 
                "N.H.",
                "M.E.",
                "ME Lat",
                "As Ind"
            ] 
            old_tags = [
                "White",
                "Whi/POC", 
                "POC", 
                "Whi/Amb", 
                "Ambig", 
                "Amb/POC", 
                "Amb/Whi", 
                "POC/Whi", 
                "POC/Amb"
            ]
            assert type(row["Race"]) == list or type(row["Race"]) == str
            if type(row["Race"]) == list:
                assert len(row["Race"]) == 2
                assert row["Race"][0] in racial_groups or row["Race"][0] == None
                assert row["Race"][1] in racial_groups or row["Race"][1] == None
            elif type(row["Race"]) == str:
                assert row["Race"] in old_tags 
                            # 👏 we're testing this without the adding white ppl lists 👏

            assert type(row["Release Date"]) == str or row["Release Date"] == None

