from src.split_values import split_raw_data_2013_2014_and_2020_to_2023, \
                                split_raw_data_2015_to_2019, \
                                split_pairings_from_fandoms

from src.get_file_paths import find_paths


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


#gotta test separate pairings from fandoms func
class TestSplitPairingsFandoms:
    def test_fandoms_does_not_mutate_input(self):
        input_list = split_raw_data_2015_to_2019("data/raw_data/ao3_2017/raw_ao3_2017_data.txt")
        split_pairings_from_fandoms(input_list)
        assert input_list == split_raw_data_2015_to_2019("data/raw_data/ao3_2017/raw_ao3_2017_data.txt")

    def test_fandoms_returns_list(self):
        input_list = split_raw_data_2015_to_2019("data/raw_data/ao3_2017/raw_ao3_2017_data.txt")
        assert type(split_pairings_from_fandoms(input_list)) == list

    def test_fandoms_returns_nested_list(self):
        input_list = split_raw_data_2015_to_2019("data/raw_data/ao3_2017/raw_ao3_2017_data.txt")
        new_list = split_pairings_from_fandoms(input_list)
        assert len(new_list) > 0
        for item in new_list:
            assert type(item) == list
        
    def test_fandoms_returns_list_of_same_length_as_input(self):
        input_list = split_raw_data_2015_to_2019("data/raw_data/ao3_2017/raw_ao3_2017_data.txt")
        new_list = split_pairings_from_fandoms(input_list)
        assert len(new_list) == len(input_list)

    def test_fandoms_returns_rows_of_number_of_columns(self):
        all_raw_data = find_paths("data/raw_data/")
        relevant_paths = [
            path for path in all_raw_data \
            if "2015" in path \
            or "2016" in path \
            or "2017" in path \
            or "2019" in path \
                ]
        for path in relevant_paths:
            input_list = split_raw_data_2015_to_2019(path)
            new_list = split_pairings_from_fandoms(input_list)
            for row in new_list:
                assert len(row) == len(new_list[0])

    def test_fandom_returns_non_pairing_non_fandom_values_unchanged(self):
        all_raw_data = find_paths("data/raw_data/")
        relevant_paths = [
            path for path in all_raw_data \
            if "2015" in path \
            or "2016" in path \
            or "2017" in path \
            or "2019" in path \
                ]
        columns_to_exclude = ["Fandom", "Ship", "Pairing", "Relationship"]
        for path in relevant_paths:
            input_list = split_raw_data_2015_to_2019(path)
            new_list = split_pairings_from_fandoms(input_list)
            for row in range(1, len(new_list)):
                for i in range(len(path[0])):
                    if path[0][i] not in columns_to_exclude:
                        assert new_list[row][i] == input_list[row][i]
    
    def test_fandom_returns_separated_pairing_and_fandom_values(self):
        all_raw_data = find_paths("data/raw_data/")
        relevant_paths = [
            path for path in all_raw_data \
            if "2016_data" not in path \
            and ("2015" in path \
            or "2016" in path \
            or "2017" in path \
            or "2019" in path) \
                ]

        for path in relevant_paths: # ones with two preceding values
            
            input_list1 = split_raw_data_2015_to_2019(path)
            new_list1 = split_pairings_from_fandoms(input_list1)
            for row in range(1, len(new_list1)):
                assert new_list1[row][2] in input_list1[row][2]
                assert new_list1[row][3] in input_list1[row][2]
                # print(">>>" + str(input_list1[row]) + " " + path)
                assert new_list1[row][2] + " " + new_list1[row][3] == input_list1[row][2]
        
        # the only one with only one preceding value
        input_list3 = split_raw_data_2015_to_2019("data/raw_data/ao3_2016/raw_ao3_2016_data.txt")
        new_list3 = split_pairings_from_fandoms(input_list3)
        for row in range(1, len(new_list3)):
            assert new_list3[row][1] in input_list3[row][1]
            assert new_list3[row][2] in input_list3[row][1]
            assert new_list3[row][1] + " " + new_list3[row][2] == input_list3[row][1]

