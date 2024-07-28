from src.util_functions.retrieve_data_from_csv import read_data_from_csv
from src.util_functions.get_file_paths import find_paths
from string import digits
import pytest

@pytest.fixture
def all_second_file_paths():
    all_paths = find_paths("data/second_clean_up_data/")
    return all_paths


class TestCsvReaderFirstCleanUpData:
    def test_1st_returns_list_of_lists(self):
        all_paths = find_paths("data/first_clean_up_data/")
        for path in all_paths:
            data_list = read_data_from_csv(path)
            assert type(data_list) == list
            for row in data_list:
                assert type(row) == list
    
    def test_1st_converts_list_items_back_to_lists(self):
        all_paths = find_paths("data/first_clean_up_data/")
        for path in all_paths:
            data_list = read_data_from_csv(path)
            for row in data_list:
                for item in row:
                    if type(item) == str:
                        assert item[0] != "["

    def test_1st_converts_none_items_back_to_none(self):
        data_list = read_data_from_csv("data/first_clean_up_data/ao3_2014/raw_ao3_2014_overall_ranking.csv")
        for row in data_list:
            if row[0] not in ["***", "New"]:
                assert row[0] == None

    def test_1st_converts_useable_integers_back_to_ints(self):
        all_paths = find_paths("data/first_clean_up_data/")
        columns_in_question = ["#", "Change", "Rank", "Fics", "Works", "New Works", "Total"]

        for path in all_paths:
            data_list = read_data_from_csv(path)
            for i in range(len(data_list[0])):
                if data_list[0][i] in columns_in_question: # if it's one of the columns we want
                    for row in data_list[1:]: # go through the whole list (minus header row)
                        is_valid_number = True
                        for char in str(row[i]):
                            if char not in digits: # if there are any non-digit characters in it
                                is_valid_number = False # it's not a number we'd've converted yet
                                break #I hope this doesn't break the enclosing loops x'D
                        if is_valid_number: # if it is a valid number
                            assert type(row[i]) == int # it should've been converted to an integer
                else: continue 
                # we don't need to waste the computer's time looking through 
                # columns we know aren't numbers

    def test_1st_returns_remaining_values_as_strings(self):
        all_paths = find_paths("data/first_clean_up_data/")
        for path in all_paths:
            data_list = read_data_from_csv(path)
            for row in data_list:
                for item in row:
                    if type(item) not in [int, list, type(None)]:
                        assert type(item) == str


class TestCsvReaderSecondCleanUpData:
    def test_2nd_converts_list_items_back_to_lists(self, all_second_file_paths):
        for path in all_second_file_paths:
            data_list = read_data_from_csv(path)

            #locating indexes
            change_index = None
            race_index = None
            type_index = None
            for column in range(len(data_list[0])):
                if data_list[0][column] == "Change":
                    change_index = column
                elif data_list[0][column] == "Relationship":
                    ship_index = column
                elif data_list[0][column] == "Race":
                    race_index = column
                elif data_list[0][column] == "Type":
                    type_index = column

            # this is pre changing "White" values to ["White", "White"]
            race_tags = [
            "White", "Whi/POC", "POC", "Whi/Amb", "Ambig", "Amb/POC", "Amb/Whi", "POC/Whi", "POC/Amb"
            ]

            for row in data_list[1:]:
                assert type(row[0]) == list
                assert len(row[0]) == 2
                assert type(row[ship_index]) == list
                assert len(row[ship_index]) >= 2
                if change_index:
                    assert type(row[change_index]) == list
                    assert len(row[change_index]) == 2
                if race_index:
                    assert (
                        type(row[race_index]) == list and len(row[race_index]) == 2
                        ) or row[race_index] in race_tags
                if type_index:
                    assert (
                        type(row[type_index]) == list and len(row[type_index]) == 2
                        ) or row[type_index] in ["Other", "Gen", "Poly"]

    def test_2nd_converts_integers_back_to_ints(self, all_second_file_paths):
        for path in all_second_file_paths:
            data_list = read_data_from_csv(path)

            new_works_index = None
            for column in range(len(data_list[0])):
                column_name = data_list[0][column]
                if column_name == "New Works":
                    new_works_index = column
                elif column_name == "Total Works":
                    total_works_index = column

            for row in data_list[1:]:
                if new_works_index:
                    assert type(row[new_works_index]) == int
                assert type(row[total_works_index]) == int

    def test_2nd_returns_remaining_values_as_strings(self, all_second_file_paths):
        for path in all_second_file_paths:
            data_list = read_data_from_csv(path)

            for row in data_list:
                for item in row:
                    if type(item) != list and type(item) != int:
                        assert type(item) == str