from src.separate_values import separate_pairings
from src.split_values import split_raw_data_2013_2014_and_2020_to_2023, split_raw_data_2015_to_2019, split_pairings_from_fandoms
from src.get_file_paths import find_paths

class TestSeparatePairings:
    #testing output list is in correct format and we didn't lose any data
    def test_separate_returns_list(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        assert type(separate_pairings(list2023)) == list

    def test_separate_returns_new_list(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        assert separate_pairings(list2023) is not list2023

    def test_separate_returns_different_list(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        assert separate_pairings(list2023) != list2023

    def test_separate_does_not_mutate_input_list(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        separate_pairings(list2023)
        assert list2023 == split_raw_data_2013_2014_and_2020_to_2023(path2023)

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2013_2014_and_2020_to_2023(femslashpath)
        separate_pairings(fem_data)
        assert fem_data == split_raw_data_2013_2014_and_2020_to_2023(femslashpath)

        old2014path = "data/raw_data/ao3_2014/raw_ao3_2014_overall_ranking.txt"
        old_data = split_raw_data_2013_2014_and_2020_to_2023(old2014path)
        separate_pairings(old_data)
        assert old_data == split_raw_data_2013_2014_and_2020_to_2023(old2014path)

        old2014fempath = "data/raw_data/ao3_2014/raw_ao3_2014_femslash_ranking.txt"
        old_fem_data = split_raw_data_2013_2014_and_2020_to_2023(old2014fempath)
        separate_pairings(old_fem_data)
        assert old_fem_data == split_raw_data_2013_2014_and_2020_to_2023(old2014fempath)
            
        old2013path = "data/raw_data/ao3_2013/raw_ao3_2013_overall_ranking.txt"
        og_data = split_raw_data_2013_2014_and_2020_to_2023(old2013path)
        separate_pairings(og_data)
        assert og_data == split_raw_data_2013_2014_and_2020_to_2023(old2013path)

    def test_separate_returns_list_of_lists(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        for a_list in separate_pairings(list2023):
            assert type(a_list) == list

    def test_separate_returns_lists_of_same_length(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for i in range(len(new_list), 8):
            assert len(new_list[i]) == len(list2023[i])

    def test_separate_returns_row_lists_of_uniform_length(self):
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
                assert len(row) == len(new_list[0])

        for path in early_paths:
            old_list1 = split_raw_data_2013_2014_and_2020_to_2023(path)
            new_list1 = separate_pairings(old_list1)
            for row in new_list1:
                assert len(row) == len(new_list1[0])

        for path in middle_paths:
            old_list_unseparated = split_raw_data_2015_to_2019(path)
            old_list2 = split_pairings_from_fandoms(old_list_unseparated)
            new_list2 = separate_pairings(old_list2)
            for row in new_list2:
                assert len(row) == len(new_list2[0])

    def test_separate_returns_items_that_did_not_contain_relevant_characters_unchanged(self):
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
        columns_to_exclude = ["Ship", "Pairing", "Pairing Tag", "Relationship", "Type", "Race"]

        for path in recent_paths:
            old_list = split_raw_data_2013_2014_and_2020_to_2023(path)
            new_list = separate_pairings(old_list)
            for row in range(1, len(new_list)):
                for i in range(len(path[0])):
                    if path[0][i] not in columns_to_exclude:
                        assert new_list[row][i] == old_list[row][i]

        for path in early_paths:
            old_list1 = split_raw_data_2013_2014_and_2020_to_2023(path)
            new_list1 = separate_pairings(old_list1)
            for row in range(1, len(new_list1)):
                for i in range(len(path[0])):
                    if path[0][i] not in columns_to_exclude:
                        assert new_list1[row][i] == old_list1[row][i]

        for path in middle_paths:
            old_list_unseparated = split_raw_data_2015_to_2019(path)
            old_list2 = split_pairings_from_fandoms(old_list_unseparated)
            new_list2 = separate_pairings(old_list2)
            for row in range(1, len(new_list2)):
                for i in range(len(path[0])):
                    if path[0][i] not in columns_to_exclude:
                        assert new_list2[row][i] == old_list2[row][i]
    
    #testing item modification was successful
    def test_separate_returns_separated_items_as_lists(self):
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
            for i in range(1, len(new_list)):
                if "/" in old_list[i][2] or "&" in old_list[i][2]: # check pairings have been separated
                    assert type(new_list[i][2]) == list
                if "/" in old_list[i][-2]: # check type tags have been separated
                    assert type(new_list[i][-2]) == list
                if "2020" not in path: # check race tags have been gathered for 2021-2023
                    assert type(new_list[i][-1]) == list
    
        for path in early_paths:
            old_list1 = split_raw_data_2013_2014_and_2020_to_2023(path)
            new_list1 = separate_pairings(old_list1)
            for i in range(1, len(new_list1)):
                if "/" in old_list1[i][1] or "&" in old_list1[i][1]: # check pairings have been separated
                    assert type(new_list1[i][1]) == list
                if "/" in old_list1[i][-3] and "femslash" not in path and "2013" not in path: # check type tags have been separated
                    assert type(new_list1[i][-3]) == list
                if "/" in old_list1[i][-2] and "2013" in path:
                    assert type(new_list1[i][-2]) == list
                #we're not separating race values for the older sets for now cause we won't 
                # be using most of em anyway & they're not in the right order anyway

        for path in middle_paths:
            old_list_unseparated = split_raw_data_2015_to_2019(path)
            old_list2 = split_pairings_from_fandoms(old_list_unseparated)
            new_list2 = separate_pairings(old_list2)
            for i in range(1, len(new_list2)):
                if "/" in old_list2[i][1] or "&" in old_list2[i][1]: # check pairings have been separated
                    assert type(new_list2[i][1]) == list
                if "/" in old_list2[i][-2]: # check type tags have been separated
                    assert type(new_list2[i][-2]) == list
                #we're not separating race values for the older sets for now cause we won't 
                # be using most of em anyway & they're not in the right order anyway

    def test_separate_separates_item_into_expected_amount_of_new_items(self):
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
            for row in new_list[1:]:
                for item in row:
                    if type(item) == list and len(item) > 2:
                        assert len(item) <= 4 # they all seem to be 4-way maximum
                    elif type(item) == list and len(item) < 2: # if it hasn't separated - aka an error
                        print(item)
                    elif type(item) == list: 
                        assert len(item) == 2
    
        for path in early_paths:
            old_list1 = split_raw_data_2013_2014_and_2020_to_2023(path)
            new_list1 = separate_pairings(old_list1)
            for row in new_list1[1:]:
                for item in row:
                    if type(item) == list and len(item) > 2:
                        assert len(item) <= 4 # they all seem to be 4-way maximum
                    elif type(item) == list and len(item) < 2: # if it hasn't separated - aka an error
                        print(item)
                    elif type(item) == list: 
                        assert len(item) == 2

        for path in middle_paths:
            old_list_unseparated = split_raw_data_2015_to_2019(path)
            old_list2 = split_pairings_from_fandoms(old_list_unseparated)
            new_list2 = separate_pairings(old_list2)
            for row in new_list2[1:]:
                for item in row:
                    if type(item) == list and len(item) > 2:
                        assert len(item) <= 4 # they all seem to be 4-way maximum
                    elif type(item) == list and len(item) < 2: # if it hasn't separated - aka an error
                        print(item)
                    elif type(item) == list: 
                        assert len(item) == 2

    def test_separate_last_item_is_a_list_after_2020(self):
        all_raw_data = find_paths("data/raw_data/")
        recent_paths = [path for path in all_raw_data if "202" in path and "2020" not in path]

        for path in recent_paths:
            old_list = split_raw_data_2013_2014_and_2020_to_2023(path)
            new_list = separate_pairings(old_list)
            for row in new_list[1:]:
                assert type(row[-1]) == list
    
    def test_separate_last_item_contains_two_strings_after_2020(self):
        all_raw_data = find_paths("data/raw_data/")
        recent_paths = [path for path in all_raw_data if "202" in path and "2020" not in path]

        for path in recent_paths:
            old_list = split_raw_data_2013_2014_and_2020_to_2023(path)
            new_list = separate_pairings(old_list)
            for row in new_list[1:]:
                assert len(row[-1]) == 2
                assert type(row[-1][0]) == str and type(row[-1][1]) == str

    def test_separate_race_values_stay_in_correct_order_after_2020(self):
        all_raw_data = find_paths("data/raw_data/")
        recent_paths = [path for path in all_raw_data if "202" in path and "2020" not in path]

        for path in recent_paths:
            old_list = split_raw_data_2013_2014_and_2020_to_2023(path)
            new_list = separate_pairings(old_list)
            for i in range(1, len(new_list)):
                assert new_list[i][-1][0] == old_list[i][-2]
                assert new_list[i][-1][1] == old_list[i][-1]

