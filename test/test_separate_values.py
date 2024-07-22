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
        columns_to_exclude = ["Ship", "Pairing", "Relationship", "Type", "Race"]

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
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for i in range(1, len(new_list)):
            if "/" in list2023[i][2] or "&" in list2023[i][2]:
                assert type(new_list[i][2]) == list
            if "/" in list2023[i][6]:
                assert type(new_list[i][6]) == list

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2013_2014_and_2020_to_2023(femslashpath)
        new_fem = separate_pairings(fem_data)
        for i in range(1, len(new_fem)):
            if "/" in fem_data[i][2] or "&" in fem_data[i][2]:
                assert type(new_fem[i][2]) == list
        
        old2014path = "data/raw_data/ao3_2014/raw_ao3_2014_overall_ranking.txt"
        old_data = split_raw_data_2013_2014_and_2020_to_2023(old2014path)
        new_old = separate_pairings(old_data)
        for i in range(1, len(new_old)):
            if "/" in old_data[i][2] or "&" in old_data[i][2]:
                assert type(new_old[i][2]) == list
            if "/" in old_data[i][-3]:
                assert type(new_old[i][-3]) == list

        old2014fempath = "data/raw_data/ao3_2014/raw_ao3_2014_femslash_ranking.txt"
        old_fem_data = split_raw_data_2013_2014_and_2020_to_2023(old2014fempath)
        new_old_fem = separate_pairings(old_fem_data)
        for i in range(1, len(new_old_fem)):
            if "/" in old_fem_data[i][1] or "&" in old_fem_data[i][1]:
                assert type(new_old_fem[i][1]) == list

        old2013path = "data/raw_data/ao3_2013/raw_ao3_2013_overall_ranking.txt"
        og_data = split_raw_data_2013_2014_and_2020_to_2023(old2013path)
        new_og_data = separate_pairings(og_data)
        for i in range(1, len(new_og_data)):
            if "/" in og_data[i][1] or "&" in og_data[i][1]:
                assert type(new_og_data[i][1]) == list
            if "/" in og_data[i][-2]:
                assert type(new_og_data[i][-2]) == list
            
    def test_separate_separates_item_into_expected_amount_of_new_items(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for i in range(1, len(new_list)):
            if "/" in list2023[i][6]:
                assert len(new_list[i][6]) == 2
        assert len(new_list[2][2]) == 2 # stranger things slash pairing
        assert len(new_list[13][2]) == 4 # minecraft gen 4 people

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2013_2014_and_2020_to_2023(femslashpath)
        new_fem = separate_pairings(fem_data)
        assert len(new_fem[2][2]) == 2 # ouat slash pairing
        assert len(new_fem[56][2]) == 3 # throuple ship

        old2014path = "data/raw_data/ao3_2014/raw_ao3_2014_overall_ranking.txt"
        old_data = split_raw_data_2013_2014_and_2020_to_2023(old2014path)
        new_old = separate_pairings(old_data)
        for i in range(1, len(new_old)):
            if "/" in old_data[i][-3]:
                assert len(new_old[i][-3]) == 2
            if "/" in old_data[i][2]:
                assert len(new_old[i][2]) == 2 
                #apparently all of 2014 overall was duos

        old2014fempath = "data/raw_data/ao3_2014/raw_ao3_2014_femslash_ranking.txt"
        old_fem_data = split_raw_data_2013_2014_and_2020_to_2023(old2014fempath)
        new_old_fem = separate_pairings(old_fem_data)
        for i in range(1, len(new_old_fem)):
            if "/" in old_fem_data[i][1]:
                assert len(new_old_fem[i][1]) == 2 
                #apparently all of 2014 overall was duos

        old2013path = "data/raw_data/ao3_2013/raw_ao3_2013_overall_ranking.txt"
        og_data = split_raw_data_2013_2014_and_2020_to_2023(old2013path)
        new_og_data = separate_pairings(og_data)
        for i in range(1, len(new_og_data)):
            if "/" in og_data[i][-2]:
                assert len(new_og_data[i][-2]) == 2
        assert len(new_og_data[2][1]) == 2
        assert len(new_og_data[115][1]) == 3

    def test_separate_last_item_is_a_list_after_2020(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for row in new_list[1:]:
            assert type(row[-1]) == list
        
        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2013_2014_and_2020_to_2023(femslashpath)
        new_fem = separate_pairings(fem_data)
        for row in new_fem[1:]:
            assert type(row[-1]) == list

    def test_separate_last_item_contains_two_strings_after_2020(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for row in new_list[1:]:
            assert len(row[-1]) == 2
            assert type(row[-1][0]) == str and type(row[-1][1]) == str

    def test_separate_race_values_stay_in_correct_order_after_2020(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for i in range(1, len(new_list)):
            assert new_list[i][-1][0] == list2023[i][7]
            assert new_list[i][-1][1] == list2023[i][8]

#TODO:       
    #figure out if separate pairings will now work on the 2015-2019 data sets 
    # & add robustness to that test suite