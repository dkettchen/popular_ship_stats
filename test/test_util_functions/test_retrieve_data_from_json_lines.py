from src.util_functions.retrieve_data_from_json_lines import get_json_lines_data
from src.util_functions.get_file_paths import find_paths
import pytest

@pytest.fixture
def all_file_paths():
    all_paths = find_paths("data/third_clean_up_data/")
    return all_paths


class TestJsonLines:
    def test_returns_list_of_dicts(self, all_file_paths):
        for filepath in all_file_paths:
            loaded_data = get_json_lines_data(filepath)

            assert type(loaded_data) == list
            for line in loaded_data:
                assert type(line) == dict

    def test_returns_dicts_with_9_expected_keys(self, all_file_paths):
        for filepath in all_file_paths:
            loaded_data = get_json_lines_data(filepath)

            for line in loaded_data:
                assert len(line) == 9
                assert list(line.keys()) == [
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

    def test_returns_dicts_with_expected_key_values(self, all_file_paths):
        for filepath in all_file_paths:
            loaded_data = get_json_lines_data(filepath)

            for item in loaded_data:
                assert type(item["Rank"]) == list
                assert len(item["Rank"]) == 2
                assert type(item["Rank"][0]) == int

                assert type(item["Change"]) == list
                assert len(item["Change"]) == 2

                assert type(item["Relationship"]) == list
                assert len(item["Relationship"]) >= 2
                for character in item["Relationship"]:
                    assert type(character) == str

                assert type(item["Fandom"]) == str
                assert type(item["New Works"]) == int or item["New Works"] == None
                assert type(item["Total Works"]) == int

                assert type(item["Type"]) == list or type(item["Type"]) == str
                if type(item["Type"]) == list:
                    assert len(item["Type"]) == 2
                assert type(item["Race"]) == list or type(item["Race"]) == str
                if type(item["Race"]) == list:
                    assert len(item["Race"]) == 2

                assert type(item["Release Date"]) == str or item["Release Date"] == None

