from src.first_cleaning_stage_code.separate_values import separate_pairings
from src.first_cleaning_stage_code.split_values import split_raw_data_2013_2014_and_2020_to_2023, split_raw_data_2015_to_2019, split_pairings_from_fandoms
from src.util_functions.get_file_paths import find_paths
from string import whitespace

#testing everything is correct after running functions, ready for first csv filing
class TestFinalTests:
    def test_no_values_have_leading_or_trailing_white_spaces(self):
        all_raw_data = find_paths("data/raw_data/")
        early_paths = [
            path for path in all_raw_data \
            if "2013_overall" in path \
            or "2014" in path
                ]
        middle_paths = [
            path for path in all_raw_data \
            if "2015" in path \
            or "2016" in path \
            or "2017" in path \
            or "2019" in path
                ]
        recent_paths = [path for path in all_raw_data if "202" in path]

        for path in recent_paths:
            old_list = split_raw_data_2013_2014_and_2020_to_2023(path)
            new_list = separate_pairings(old_list)
            for row in new_list:
                for item in row:
                    if type(item) == list:
                        for value in item:
                            assert value[-1] not in whitespace
                            assert value[0] not in whitespace
                    else: 
                        assert item[-1] not in whitespace
                        assert item[0] not in whitespace
    
        for path in early_paths:
            old_list1 = split_raw_data_2013_2014_and_2020_to_2023(path)
            new_list1 = separate_pairings(old_list1)
            for row in new_list1:
                for item in row:
                    if "2014_overall" in path:
                        if item != "":
                            assert item[-1] not in whitespace
                            assert item[0] not in whitespace
                    else: 
                        assert item[-1] not in whitespace
                        assert item[0] not in whitespace

        for path in middle_paths:
            old_list_unseparated = split_raw_data_2015_to_2019(path)
            old_list2 = split_pairings_from_fandoms(old_list_unseparated)
            new_list2 = separate_pairings(old_list2)
            for row in new_list2:
                for item in row:
                    assert item[-1] not in whitespace
                    assert item[0] not in whitespace


