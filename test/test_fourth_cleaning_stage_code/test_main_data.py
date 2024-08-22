from src.util_functions.get_file_paths import find_paths
import pytest
from json import load

@pytest.fixture
def all_paths():
    all_paths = find_paths("data/fourth_clean_up_data/")
    return all_paths

@pytest.fixture
def all_data(all_paths):
    """
    creates a list of dictionaries containing the filepath to 
    and data contained in all fourth stage main set files
    """
    all_data = []
    for path in all_paths:
        with open(path, "r") as file:
            data_list = load(file)
            data_dict = {
                "path": path,
                "data": data_list
            }
            all_data.append(data_dict)
        
    return all_data

@pytest.fixture
def all_clean_fandoms():
    path = "data/reference_and_test_files/cleaning_fandoms/unified_abbr_fandoms_list.json"
    with open(path, "r") as fandom_file:
        all_fandoms = list(load(fandom_file).keys())
    return all_fandoms

@pytest.fixture
def all_old_fandoms():
    path = "data/reference_and_test_files/cleaning_fandoms/unified_abbr_fandoms_list.json"
    with open(path, "r") as fandom_file:
        all_fandoms = load(fandom_file)
    old_fandoms = []
    for key in all_fandoms:
        old_fandoms.extend(all_fandoms[key])
    return old_fandoms

@pytest.fixture
def all_clean_characters():
    path = "data/reference_and_test_files/cleaning_characters/unified_abbr_characters_list.json"
    with open(path, "r") as char_file:
        char_file_contents = load(char_file)
    all_characters = []
    for key in char_file_contents:
        character_list = list(char_file_contents[key].keys())
        all_characters.extend(character_list)
    return all_characters

@pytest.fixture
def all_old_characters():
    path = "data/reference_and_test_files/cleaning_characters/unified_abbr_characters_list.json"
    with open(path, "r") as char_file:
        char_file_contents = load(char_file)
    all_old_characters = []
    for key in char_file_contents:
        for character in char_file_contents[key]:
            character_list = char_file_contents[key][character]["op_versions"]
            all_old_characters.extend(character_list)
    return all_old_characters

@pytest.fixture
def all_old_data():
    all_paths = find_paths("data/third_clean_up_data/")
    all_data = []
    for path in all_paths:
        with open(path, "r") as file:
            data_list = load(file)
            data_dict = {
                "path": path,
                "data": data_list
            }
            all_data.append(data_dict)
        
    return all_data


def test_is_list_of_dicts(all_data):
    for data_set in all_data:
        path = data_set["path"]
        data = data_set["data"]

        assert type(data) == list
        for row in data:
            assert type(row) == dict

def test_number_of_rows_is_unchanged(all_data):
    for data_set in all_data:
        path = data_set["path"]
        data = data_set["data"]

        if "2021_femslash" in path:
            assert len(data) == 101
        elif "2015_femslash" in path:
            assert len(data) == 102
        elif "2014_femslash" in path:
            assert len(data) == 50
        elif "2013" in path:
            assert len(data) == 161
        else:
            assert len(data) == 100

def test_each_row_contains_expected_number_of_keys(all_data):
    for data_set in all_data:
        path = data_set["path"]
        data = data_set["data"]

        for row in data:
            assert len(row.keys()) == 12

def test_each_row_has_expected_key_names(all_data):
    for data_set in all_data:
        path = data_set["path"]
        data = data_set["data"]
        expected_keys = [
            "Rank",
            "Change",
            "Relationship",
            "Fandom",
            "New Works",
            "Total Works",
            "Type",
            "Race",
            "Release Date",
            "Old Fandom",
            "Old Characters",
            "RPF or Fic"
        ]

        for row in data:
            assert list(row.keys()) == expected_keys

def test_each_row_key_value_is_expected_type(all_data):
    for data_set in all_data:
        path = data_set["path"]
        data = data_set["data"]

        for row in data:
            for key in [
                "Rank",
                "Change",
                "Relationship",
                "Old Characters",
            ]:
                assert type(row[key]) == list
            for key in [
                "Fandom",
                "Old Fandom",
                "RPF or Fic"
            ]: 
                assert type(row[key]) == str
            for key in [
                "Type",
                "Race",
            ]:
                assert type(row[key]) == list or type(row[key]) == str
            assert type(row["Total Works"]) == int
            assert type(row["New Works"]) == int or not row["New Works"]
            assert type(row["Release Date"]) == str or not row["Release Date"]


def test_fandom_is_a_clean_fandom_name(all_data, all_clean_fandoms):
    for data_set in all_data:
        path = data_set["path"]
        data = data_set["data"]

        for row in data:
            assert row["Fandom"] in all_clean_fandoms

def test_old_fandom_contains_old_fandom_name(all_data, all_old_fandoms):
    for data_set in all_data:
        path = data_set["path"]
        data = data_set["data"]

        for row in data:
            if row["Old Fandom"] != "Rogue One: A Star Wars Story (2016)":
                assert row["Old Fandom"] in all_old_fandoms

def test_relationship_list_is_not_empty(all_data):
    for data_set in all_data:
        path = data_set["path"]
        data = data_set["data"]

        for row in data:
            assert len(row["Relationship"]) > 0

def test_relationship_contains_clean_names(all_data, all_clean_characters):
    for data_set in all_data:
        path = data_set["path"]
        data = data_set["data"]

        for row in data:
            for character in row["Relationship"]:
                assert character in all_clean_characters

def test_old_characters_contain_old_names(all_data,all_old_characters):
    for data_set in all_data:
        path = data_set["path"]
        data = data_set["data"]

        for row in data:
            for character in row["Old Characters"]:
                assert character in all_old_characters

def test_rpf_fic_key_has_expected_values(all_data):
    for data_set in all_data:
        path = data_set["path"]
        data = data_set["data"]

        for row in data:
            assert row["RPF or Fic"] in ["RPF", "fictional"]

def test_remaining_values_are_unchanged(all_data, all_old_data):
    for index in range(len(all_data)):
        data_set = all_data[index]
        old_data_set = all_old_data[index]
        path = data_set["path"]
        data = data_set["data"]
        old_path = old_data_set["path"]
        old_data = old_data_set["data"]

        for row_index in range(len(data)):
            for key in [
            "Rank",
            "Change",
            "New Works",
            "Total Works",
            "Type",
            "Race",
            "Release Date",
            ]:
                assert data[row_index][key] == old_data[row_index][key]
