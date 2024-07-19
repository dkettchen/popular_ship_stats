from src.formatting_data import split_raw_data_2020_to_2023, separate_pairings, find_paths

class TestSplitRecentDataSets:
    def test_does_not_mutate_input_string(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        split_raw_data_2020_to_2023(path2023)
        assert path2023 == "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        split_raw_data_2020_to_2023(femslashpath)
        assert femslashpath == "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"

    #testing list is in correct format
    def test_returns_list(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        assert type(split_raw_data_2020_to_2023(path2023)) == list
    
    def test_returns_list_of_lists(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        for a_list in split_raw_data_2020_to_2023(path2023):
            assert type(a_list) == list

    def test_returns_list_of_column_length(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2020_to_2023(path2023)
        for item in data_list[1:]:
            assert len(item) == len(data_list[0]) + 1
                                #because apparently "race" has 1 title and two values

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2020_to_2023(femslashpath)
        for item in fem_data[1:]:
            assert len(item) == len(fem_data[0]) + 1
    
    def test_returns_nested_list_of_strings(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2020_to_2023(path2023)
        for item in data_list:
            for value in item:
                assert type(value) == str
    
    #testing values were separated correctly
    def test_expected_number_values_are_number_strings(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2020_to_2023(path2023)
        for item in data_list[1:]:
            assert type(int(item[4])) == int
            assert type(int(item[5])) == int
            if item[0][-1] == "=": 
                assert type(int(item[0][0:-1])) == int
            else: assert type(int(item[0])) == int

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2020_to_2023(femslashpath)
        for item in fem_data[1:]:
            assert type(int(item[4])) == int
            if item[0][-1] == "=": 
                assert type(int(item[0][0:-1])) == int
            else: assert type(int(item[0])) == int

    def test_pairing_labels_are_expected_format(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2020_to_2023(path2023)
        pairing_tags = ["M/M", "F/F", "F/M", "Gen", "Other"] 
        for item in data_list[1:]:
            assert item[6] in pairing_tags
    
    def test_race_labels_are_expected_format(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2020_to_2023(path2023)
        race_tags = [
            "White", "MENA", "Asian", "Indig", "Latino", 
            "Ambig", "Af Lat", "Black", "N.H.", "ME Lat",
            "As Ind"
            ]
        for item in data_list[1:]:
            assert item[7] in race_tags
            assert item[8] in race_tags

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2020_to_2023(femslashpath)
        for item in fem_data[1:]:
            assert item[5] in race_tags
            assert item[6] in race_tags

    def test_pairings_contain_slash_or_ampercent(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2020_to_2023(path2023)
        for item in data_list[1:]:
            assert "/" in item[2] or "&" in item[2]

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2020_to_2023(femslashpath)
        for item in fem_data[1:]:
            assert "/" in item[2] or "&" in item[2]
    
    def test_change_contains_number_with_plus_or_minus_OR_is_new(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        data_list = split_raw_data_2020_to_2023(path2023)
        for item in data_list[1:]:
            assert item[1] == "New" or item[1][0] == "+" or item[1][0] == "-"
            if item[1] != "New":
                assert type(int(item[1][1:])) == int

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2020_to_2023(femslashpath)
        for item in fem_data[1:]:
            assert item[1] == "New" or item[1][0] == "+" or item[1][0] == "-"
            if item[1] != "New":
                assert type(int(item[1][1:])) == int

class TestSeparatePairings:
    #testing output list is in correct format and we didn't lose any data
    def test_returns_list(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        assert type(separate_pairings(list2023)) == list

    def test_returns_new_list(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        assert separate_pairings(list2023) is not list2023

    def test_returns_different_list(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        assert separate_pairings(list2023) != list2023

    def test_does_not_mutate_input_list(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        separate_pairings(list2023)
        assert list2023 == split_raw_data_2020_to_2023(path2023)

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2020_to_2023(femslashpath)
        separate_pairings(fem_data)
        assert fem_data == split_raw_data_2020_to_2023(femslashpath)
    
    def test_returns_list_of_lists(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        for a_list in separate_pairings(list2023):
            assert type(a_list) == list

    def test_returns_lists_of_same_length(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for i in range(len(new_list), 8):
            assert len(new_list[i]) == len(list2023[i])

    def test_returns_row_lists_of_uniform_length(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for i in range(1, len(new_list)):
            assert len(new_list[i]) == len(new_list[0])

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2020_to_2023(femslashpath)
        new_fem = separate_pairings(fem_data)
        for i in range(1, len(new_fem)):
            assert len(new_fem[i]) == len(new_fem[0])

    def test_returns_items_that_did_not_contain_relevant_characters_unchanged(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        index_list = [0,1,3,4,5]
        for row in range(1, len(new_list)):
            for i in index_list:
                assert new_list[row][i] == list2023[row][i]

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2020_to_2023(femslashpath)
        new_fem = separate_pairings(fem_data)
        fem_index_list = [0,1,3,4]
        for row in range(1, len(new_fem)):
            for i in fem_index_list:
                assert new_list[row][i] == list2023[row][i]
    
    #testing item modification was successful
    def test_returns_separated_items_as_lists(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for i in range(1, len(new_list)):
            if "/" in list2023[i][2] or "&" in list2023[i][2]:
                assert type(new_list[i][2]) == list
            if "/" in list2023[i][6]:
                assert type(new_list[i][6]) == list

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2020_to_2023(femslashpath)
        new_fem = separate_pairings(fem_data)
        for i in range(1, len(new_fem)):
            if "/" in list2023[i][2] or "&" in list2023[i][2]:
                assert type(new_fem[i][2]) == list

    def test_separates_item_into_expected_amount_of_new_items(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for i in range(1, len(new_list)):
            if "/" in list2023[i][6]:
                assert len(new_list[i][6]) == 2
        assert len(new_list[2][2]) == 2 # stranger things slash pairing
        assert len(new_list[13][2]) == 4 # minecraft gen 4 people

        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2020_to_2023(femslashpath)
        new_fem = separate_pairings(fem_data)
        assert len(new_fem[2][2]) == 2 # ouat slash pairing
        assert len(new_fem[56][2]) == 3 # throuple ship

    def test_last_item_is_a_list(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for row in new_list[1:]:
            assert type(row[-1]) == list
        
        femslashpath = "data/raw_data/ao3_2023/raw_ao3_2023_femslash_ranking.txt"
        fem_data = split_raw_data_2020_to_2023(femslashpath)
        new_fem = separate_pairings(fem_data)
        for row in new_fem[1:]:
            assert type(row[-1]) == list

    def test_last_item_contains_two_strings(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for row in new_list[1:]:
            assert len(row[-1]) == 2
            assert type(row[-1][0]) == str and type(row[-1][1]) == str

    def test_race_values_stay_in_correct_order(self):
        path2023 = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        list2023 = split_raw_data_2020_to_2023(path2023)
        new_list = separate_pairings(list2023)
        for i in range(1, len(new_list)):
            assert new_list[i][-1][0] == list2023[i][7]
            assert new_list[i][-1][1] == list2023[i][8]

class TestFindPaths:
    def test_returns_list(self):
        assert type(find_paths("data/raw_data/")) == list

    def test_returns_non_empty_list(self):
        assert len(find_paths("data/raw_data/")) > 0

    def test_returns_list_of_strings(self):
        for item in find_paths("data/raw_data/"):
            assert type(item) == str
    
    def test_returns_data_folder_file_paths(self):
        for item in find_paths("data/raw_data/"):
            assert "data/" in item

    def test_returns_expected_file_paths(self):
        assert "data/raw_data/ao3_2023/raw_ao3_2023_data.txt" in find_paths("data/raw_data/")
        assert "data/raw_data/ao3_2013/raw_ao3_2013_fandoms.txt" in find_paths("data/raw_data/")
        assert "data/raw_data/ao3_2016/raw_ao3_2016_femslash_ranking.txt" in find_paths("data/raw_data/")

    