from src.formatting_data import split_raw_data_2013_2014_and_2020_to_2023, separate_pairings, find_paths, split_raw_data_2015_to_2019

class TestFindPaths:
    def test_find_returns_list(self):
        assert type(find_paths("data/raw_data/")) == list

    def test_find_returns_non_empty_list(self):
        assert len(find_paths("data/raw_data/")) > 0

    def test_find_returns_list_of_strings(self):
        for item in find_paths("data/raw_data/"):
            assert type(item) == str
    
    def test_find_returns_data_folder_file_paths(self):
        for item in find_paths("data/raw_data/"):
            assert "data/" in item

    def test_find_returns_expected_file_paths(self):
        assert "data/raw_data/ao3_2023/raw_ao3_2023_data.txt" in find_paths("data/raw_data/")
        assert "data/raw_data/ao3_2013/raw_ao3_2013_fandoms.txt" in find_paths("data/raw_data/")
        assert "data/raw_data/ao3_2016/raw_ao3_2016_femslash_ranking.txt" in find_paths("data/raw_data/")


class TestSplitRecentAndOldDataSets:
    def test_split_does_not_mutate_input_string(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        split_raw_data_2013_2014_and_2020_to_2023(path2023)
        assert path2023 == "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        split_raw_data_2013_2014_and_2020_to_2023(femslashpath)
        assert femslashpath == "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"

        oldpath = "data/raw_data/ao3_2014/raw_ao3_2014_overall_ranking.txt"
        split_raw_data_2013_2014_and_2020_to_2023(oldpath)
        assert oldpath == "data/raw_data/ao3_2014/raw_ao3_2014_overall_ranking.txt"

    #testing list is in correct format
    def test_split_returns_list(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        assert type(split_raw_data_2013_2014_and_2020_to_2023(path2023)) == list
    
    def test_split_returns_list_of_lists(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        for a_list in split_raw_data_2013_2014_and_2020_to_2023(path2023):
            assert type(a_list) == list

    def test_split_returns_list_of_column_length(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        for item in data_list[1:]:
            assert len(item) == len(data_list[0]) + 1
                                #because apparently "race" has 1 title and two values

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2013_2014_and_2020_to_2023(femslashpath)
        for item in fem_data[1:]:
            assert len(item) == len(fem_data[0]) + 1

        old2014path = "data/raw_data/ao3_2014/raw_ao3_2014_overall_ranking.txt"
        old_data = split_raw_data_2013_2014_and_2020_to_2023(old2014path)
        for item in old_data[1:]:
            assert len(item) == len(old_data[0])

        old2014fempath = "data/raw_data/ao3_2014/raw_ao3_2014_femslash_ranking.txt"
        old_fem_data = split_raw_data_2013_2014_and_2020_to_2023(old2014fempath)
        for item in old_fem_data[1:]:
            assert len(item) == len(old_fem_data[0])

        old2013path = "data/raw_data/ao3_2013/raw_ao3_2013_overall_ranking.txt"
        og_data = split_raw_data_2013_2014_and_2020_to_2023(old2013path)
        for item in og_data[1:]:
            assert len(item) == len(og_data[0])
    
    def test_split_returns_nested_list_of_strings(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        for item in data_list:
            for value in item:
                assert type(value) == str
    
    #testing values were separated correctly
    def test_split_expected_number_values_are_number_strings(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        for item in data_list[1:]:
            assert type(int(item[4])) == int
            assert type(int(item[5])) == int
            if item[0][-1] == "=": 
                assert type(int(item[0][0:-1])) == int
            else: assert type(int(item[0])) == int

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2013_2014_and_2020_to_2023(femslashpath)
        for item in fem_data[1:]:
            assert type(int(item[4])) == int
            if item[0][-1] == "=": 
                assert type(int(item[0][0:-1])) == int
            else: assert type(int(item[0])) == int

        old2014path = "data/raw_data/ao3_2014/raw_ao3_2014_overall_ranking.txt"
        old_data = split_raw_data_2013_2014_and_2020_to_2023(old2014path)
        for item in old_data[1:]:
            if item[1][0] == "=": 
                assert type(int(item[1][1:])) == int
            else: assert type(int(item[1])) == int
            assert type(int(item[-1])) == int

        old2014fempath = "data/raw_data/ao3_2014/raw_ao3_2014_femslash_ranking.txt"
        old_fem_data = split_raw_data_2013_2014_and_2020_to_2023(old2014fempath)
        for item in old_fem_data[1:]:
            if item[0][0] == "=": 
                assert type(int(item[0][1:])) == int
            else: assert type(int(item[0])) == int
            assert type(int(item[-1])) == int
            
        old2013path = "data/raw_data/ao3_2013/raw_ao3_2013_overall_ranking.txt"
        og_data = split_raw_data_2013_2014_and_2020_to_2023(old2013path)
        for item in og_data[1:]:
            assert type(int(item[0])) == int
            assert type(int(item[-1])) == int

    def test_split_pairing_labels_are_expected_format(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        pairing_tags = ["M/M", "F/F", "F/M", "Gen", "Other"] 
        for item in data_list[1:]:
            assert item[6] in pairing_tags
    
    def test_split_race_labels_are_expected_format(self):
        race_tags = [
            "White", "MENA", "Asian", "Indig", "Latino", 
            "Ambig", "Af Lat", "Black", "N.H.", "ME Lat",
            "As Ind"
            ]
        old_race_tags = [
            "White", "Whi/POC", "POC", "Whi/Amb", "Ambig", "Amb/POC", "Amb/Whi", "POC/Whi", "POC/Amb"
            ]

        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        for item in data_list[1:]:
            assert item[7] in race_tags
            assert item[8] in race_tags

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2013_2014_and_2020_to_2023(femslashpath)
        for item in fem_data[1:]:
            assert item[5] in race_tags
            assert item[6] in race_tags

        old2014path = "data/raw_data/ao3_2014/raw_ao3_2014_overall_ranking.txt"
        old_data = split_raw_data_2013_2014_and_2020_to_2023(old2014path)
        for item in old_data[1:]:
            assert item[-2] in old_race_tags

    def test_split_pairings_contain_slash_or_ampercent(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        for item in data_list[1:]:
            assert "/" in item[2] or "&" in item[2]

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2013_2014_and_2020_to_2023(femslashpath)
        for item in fem_data[1:]:
            assert "/" in item[2] or "&" in item[2]
        
        old2014path = "data/raw_data/ao3_2014/raw_ao3_2014_overall_ranking.txt"
        old_data = split_raw_data_2013_2014_and_2020_to_2023(old2014path)
        for item in old_data[1:]:
            assert "/" in item[2] or "&" in item[2]

        old2014fempath = "data/raw_data/ao3_2014/raw_ao3_2014_femslash_ranking.txt"
        old_fem_data = split_raw_data_2013_2014_and_2020_to_2023(old2014fempath)
        for item in old_fem_data[1:]:
            assert "/" in item[1] or "&" in item[1]
            
        old2013path = "data/raw_data/ao3_2013/raw_ao3_2013_overall_ranking.txt"
        og_data = split_raw_data_2013_2014_and_2020_to_2023(old2013path)
        for item in og_data[1:]:
            assert "/" in item[1] or "&" in item[1]

    def test_split_change_contains_number_with_plus_or_minus_OR_is_new(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        for item in data_list[1:]:
            assert item[1] == "New" or item[1][0] == "+" or item[1][0] == "-"
            if item[1] != "New":
                assert type(int(item[1][1:])) == int

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2013_2014_and_2020_to_2023(femslashpath)
        for item in fem_data[1:]:
            assert item[1] == "New" or item[1][0] == "+" or item[1][0] == "-"
            if item[1] != "New":
                assert type(int(item[1][1:])) == int
        
    def test_split_change_contains_asterixes_or_is_empty_for_2014(self):
        old2014path = "data/raw_data/ao3_2014/raw_ao3_2014_overall_ranking.txt"
        old_data = split_raw_data_2013_2014_and_2020_to_2023(old2014path)
        for item in old_data[1:]:
            assert item[0] == "***" or item[0] == ""


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
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for i in range(1, len(new_list)):
            assert len(new_list[i]) == len(new_list[0])

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2013_2014_and_2020_to_2023(femslashpath)
        new_fem = separate_pairings(fem_data)
        for i in range(1, len(new_fem)):
            assert len(new_fem[i]) == len(new_fem[0])

        old2014path = "data/raw_data/ao3_2014/raw_ao3_2014_overall_ranking.txt"
        old_data = split_raw_data_2013_2014_and_2020_to_2023(old2014path)
        new_old = separate_pairings(old_data)
        for i in range(1, len(new_old)):
            assert len(new_old[i]) == len(new_old[0])

        old2014fempath = "data/raw_data/ao3_2014/raw_ao3_2014_femslash_ranking.txt"
        old_fem_data = split_raw_data_2013_2014_and_2020_to_2023(old2014fempath)
        new_old_fem = separate_pairings(old_fem_data)
        for i in range(1, len(new_old_fem)):
            assert len(new_old_fem[i]) == len(new_old_fem[0])

        old2013path = "data/raw_data/ao3_2013/raw_ao3_2013_overall_ranking.txt"
        og_data = split_raw_data_2013_2014_and_2020_to_2023(old2013path)
        new_og_data = separate_pairings(og_data)
        for i in range(1, len(new_og_data)):
            assert len(new_og_data[i]) == len(new_og_data[0])

    def test_separate_returns_items_that_did_not_contain_relevant_characters_unchanged(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2013_2014_and_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        index_list = [0,1,3,4,5]
        for row in range(1, len(new_list)):
            for i in index_list:
                assert new_list[row][i] == list2023[row][i]

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2013_2014_and_2020_to_2023(femslashpath)
        new_fem = separate_pairings(fem_data)
        fem_index_list = [0,1,3,4]
        for row in range(1, len(new_fem)):
            for i in fem_index_list:
                assert new_fem[row][i] == fem_data[row][i]

        old2014path = "data/raw_data/ao3_2014/raw_ao3_2014_overall_ranking.txt"
        old_data = split_raw_data_2013_2014_and_2020_to_2023(old2014path)
        new_old = separate_pairings(old_data)
        index_list_2014 = [0,1,3,5,6]
        for row in range(1, len(new_old)):
            for i in index_list_2014:
                assert new_old[row][i] == old_data[row][i]

        old2014fempath = "data/raw_data/ao3_2014/raw_ao3_2014_femslash_ranking.txt"
        old_fem_data = split_raw_data_2013_2014_and_2020_to_2023(old2014fempath)
        new_old_fem = separate_pairings(old_fem_data)
        fem_index_list_2014 = [0,2,3]
        for row in range(1, len(new_old_fem)):
            for i in fem_index_list_2014:
                assert new_old_fem[row][i] == old_fem_data[row][i]

        old2013path = "data/raw_data/ao3_2013/raw_ao3_2013_overall_ranking.txt"
        og_data = split_raw_data_2013_2014_and_2020_to_2023(old2013path)
        new_og_data = separate_pairings(og_data)
        index_list_2013 = [0,2,4]
        for row in range(1, len(new_og_data)):
            for i in index_list_2013:
                assert new_og_data[row][i] == og_data[row][i]
    
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


class TestSplitMiddleDataSets:
    def test_middle_does_not_mutate_input_string(self):
        path2016 = "data/raw_data/ao3_2016/raw_ao3_2016_data.txt"
        split_raw_data_2015_to_2019(path2016)
        assert path2016 == "data/raw_data/ao3_2016/raw_ao3_2016_data.txt"

    #testing list is in correct format
    def test_middle_returns_list(self):
        path2016 = "data/raw_data/ao3_2016/raw_ao3_2016_data.txt"
        assert type(split_raw_data_2015_to_2019(path2016)) == list

    def test_middle_returns_list_of_lists(self):
        path2016 = "data/raw_data/ao3_2016/raw_ao3_2016_data.txt"
        data_2016 = split_raw_data_2015_to_2019(path2016)
        for row in data_2016:
            assert type(row) == list

    def test_middle_returns_rows_of_strings(self):
        path2016 = "data/raw_data/ao3_2016/raw_ao3_2016_data.txt"
        data_2016 = split_raw_data_2015_to_2019(path2016)
        for row in data_2016:
            for value in row:
                assert type(value) == str

    def test_middle_returns_rows_of_column_length_minus_one(self):
        path2016 = "data/raw_data/ao3_2016/raw_ao3_2016_data.txt"
        data_2016 = split_raw_data_2015_to_2019(path2016)
        for row in data_2016[1:]:
            assert len(row) == len(data_2016[0]) -1

        fempath2019 = "data/raw_data/ao3_2019/raw_ao3_2019_femslash_ranking.txt"
        data_2019 = split_raw_data_2015_to_2019(fempath2019)
        for row in data_2019[1:]:
            assert len(row) == len(data_2019[0]) -1

        overallpath2015 = "data/raw_data/ao3_2015/raw_ao3_2015_overall_ranking.txt"
        overall_data_2015 = split_raw_data_2015_to_2019(overallpath2015)
        for row in overall_data_2015[1:]:
            assert len(row) == len(overall_data_2015[0]) -1
        
        path2017 = "data/raw_data/ao3_2017/raw_ao3_2017_data.txt"
        data_2017 = split_raw_data_2015_to_2019(path2017)
        for row in data_2017[1:]:
            assert len(row) == len(data_2017[0]) -1

    #testing values were separated correctly
    def test_middle_expected_numbers_are_number_strings(self):
        path2016 = "data/raw_data/ao3_2016/raw_ao3_2016_data.txt"
        data_2016 = split_raw_data_2015_to_2019(path2016)
        for item in data_2016[1:]:
            assert type(int(item[-3][-3:])) == int
            assert type(int(item[-4][-3:])) == int
            if item[0][-1] == "=": 
                assert type(int(item[0][:-1])) == int
            else: assert type(int(item[0])) == int

        fempath2019 = "data/raw_data/ao3_2019/raw_ao3_2019_femslash_ranking.txt"
        data_2019 = split_raw_data_2015_to_2019(fempath2019)
        for item in data_2019[1:]:
            assert type(int(item[-2][-3:])) == int
            if item[0][-1] == "=": 
                assert type(int(item[0][:-1])) == int
            else: assert type(int(item[0])) == int

        overallpath2015 = "data/raw_data/ao3_2015/raw_ao3_2015_overall_ranking.txt"
        overall_data_2015 = split_raw_data_2015_to_2019(overallpath2015)
        for item in overall_data_2015[1:]:
            assert type(int(item[0])) == int
            assert type(int(item[-3][-3:])) == int
        
        path2017 = "data/raw_data/ao3_2017/raw_ao3_2017_data.txt"
        data_2017 = split_raw_data_2015_to_2019(path2017)
        for item in data_2017[1:]:
            assert type(int(item[-3][-3:])) == int
            assert type(int(item[-4][-3:])) == int
            if item[0][-1] == "=": 
                assert type(int(item[0][:-1])) == int
            else: assert type(int(item[0])) == int

    def test_middle_pairing_labels_are_expected_format(self):
        pairing_tags = ["M/M", "F/F", "F/M", "Gen", "Other"] 

        path2016 = "data/raw_data/ao3_2016/raw_ao3_2016_data.txt"
        data_2016 = split_raw_data_2015_to_2019(path2016)
        for item in data_2016[1:]:
            assert item[4] in pairing_tags

        overallpath2015 = "data/raw_data/ao3_2015/raw_ao3_2015_overall_ranking.txt"
        overall_data_2015 = split_raw_data_2015_to_2019(overallpath2015)
        for item in overall_data_2015[1:]:
            assert item[4] in pairing_tags
        
        path2017 = "data/raw_data/ao3_2017/raw_ao3_2017_data.txt"
        data_2017 = split_raw_data_2015_to_2019(path2017)
        for item in data_2017[1:]:
            assert item[-2] in pairing_tags

    def test_middle_race_labels_are_expected_format(self):
        old_race_tags = [
            "White", "Whi/POC", "POC", "Whi/Amb", "Ambig", "Amb/POC", "Amb/Whi", "POC/Whi", "POC/Amb"
            ]
        
        path2016 = "data/raw_data/ao3_2016/raw_ao3_2016_data.txt"
        data_2016 = split_raw_data_2015_to_2019(path2016)
        for item in data_2016[1:]:
            assert item[-1] in old_race_tags

        fempath2019 = "data/raw_data/ao3_2019/raw_ao3_2019_femslash_ranking.txt"
        data_2019 = split_raw_data_2015_to_2019(fempath2019)
        for item in data_2019[1:]:
            assert item[-1] in old_race_tags

        overallpath2015 = "data/raw_data/ao3_2015/raw_ao3_2015_overall_ranking.txt"
        overall_data_2015 = split_raw_data_2015_to_2019(overallpath2015)
        for item in overall_data_2015[1:]:
            assert item[-1] in old_race_tags

        path2017 = "data/raw_data/ao3_2017/raw_ao3_2017_data.txt"
        data_2017 = split_raw_data_2015_to_2019(path2017)
        for item in data_2017[1:]:
            assert item[-1] in old_race_tags

    def test_middle_pairings_contain_slash_or_ampercent(self):
        path2016 = "data/raw_data/ao3_2016/raw_ao3_2016_data.txt"
        data_2016 = split_raw_data_2015_to_2019(path2016)
        for item in data_2016[1:]:
            assert "/" in item[1] or "&" in item[1]

        fempath2019 = "data/raw_data/ao3_2019/raw_ao3_2019_femslash_ranking.txt"
        data_2019 = split_raw_data_2015_to_2019(fempath2019)
        for item in data_2019[1:]:
            assert "/" in item[2] or "&" in item[2]

        overallpath2015 = "data/raw_data/ao3_2015/raw_ao3_2015_overall_ranking.txt"
        overall_data_2015 = split_raw_data_2015_to_2019(overallpath2015)
        for item in overall_data_2015[1:]:
            assert "/" in item[2] or "&" in item[2]

        path2017 = "data/raw_data/ao3_2017/raw_ao3_2017_data.txt"
        data_2017 = split_raw_data_2015_to_2019(path2017)
        for item in data_2017[1:]:
            assert "/" in item[2] or "&" in item[2]

    def test_middle_change_contains_number_with_plus_or_minus_is_number_OR_is_N(self):
        fempath2019 = "data/raw_data/ao3_2019/raw_ao3_2019_femslash_ranking.txt"
        data_2019 = split_raw_data_2015_to_2019(fempath2019)
        for item in data_2019[1:]:
            assert item[1] == "N" or item[1][0] == "+" or item[1][0] == "-" or type(int(item[1])) == int 
            if item[1][0] == "+" or item[1][0] == "-":
                assert type(int(item[1][1:])) == int

        overallpath2015 = "data/raw_data/ao3_2015/raw_ao3_2015_overall_ranking.txt"
        overall_data_2015 = split_raw_data_2015_to_2019(overallpath2015)
        for item in overall_data_2015[1:]:
            assert item[1] == "N" or item[1][0] == "+" or item[1][0] == "-" or type(int(item[1])) == int 
            if item[1][0] == "+" or item[1][0] == "-":
                assert type(int(item[1][1:])) == int

        path2017 = "data/raw_data/ao3_2017/raw_ao3_2017_data.txt"
        data_2017 = split_raw_data_2015_to_2019(path2017)
        for item in data_2017[1:]:
            assert item[1] == "N" or item[1][0] == "+" or item[1][0] == "-" or type(int(item[1])) == int 
            if item[1][0] == "+" or item[1][0] == "-":
                assert type(int(item[1][1:])) == int

    