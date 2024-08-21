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




    # I can already see we're missing minecrafter rpf from our abbr char list :l
    # dunno where they got lost in the cleaning process, we'll have to fix that
        # it did update "Youtube" as their fandom, so the fandoms are fine

def test_each_row_contains_expected_number_of_keys(all_data):
    for data_set in all_data:
        path = data_set["path"]
        data = data_set["data"]

        for row in data:
            assert len(row.keys()) == 12

# check there's the expected number of keys (old keys + 3)
# check everything's the expected type etc

# check fandom is in our clean fandom list (make list?)

# check relationship key is not empty
# check relationship value only contains names in our full names list (make list?)

# check there is a rpf/fic key
# check its value is either "RPF" or "fictional"

# check new "old" keys have been added
# check old keys contain original values

# check remaining keys & values have not been changed