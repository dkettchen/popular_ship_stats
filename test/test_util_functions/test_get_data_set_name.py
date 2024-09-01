from src.util_functions.get_data_set_name import get_data_set_name

def test_does_not_mutate_input():
    filepath = "data/data_set_ao3_2023_femslash"
    get_data_set_name(filepath)
    assert filepath == "data/data_set_ao3_2023_femslash"

def test_returns_string():
    filepath = "data/first_clean_up_data/ao3_2013/raw_ao3_2013_overall_ranking.csv"
    result = get_data_set_name(filepath)
    assert type(result) == str

def test_returns_new_string():
    filepath = "data/first_clean_up_data/ao3_2013/raw_ao3_2013_overall_ranking.csv"
    result = get_data_set_name(filepath)
    assert result != filepath

def test_returns_a_data_set_name():
    data_sets_list = [
        "AO3_2013_overall",
        "AO3_2014_femslash",
        "AO3_2014_overall",
        "AO3_2015_femslash",
        "AO3_2015_overall",
        "AO3_2016_data",
        "AO3_2016_femslash",
        "AO3_2016_overall",
        "AO3_2017_data",
        "AO3_2017_femslash",
        "AO3_2017_overall",
        "AO3_2019_data",
        "AO3_2019_femslash",
        "AO3_2019_overall",
        "AO3_2020_data",
        "AO3_2020_femslash",
        "AO3_2020_overall",
        "AO3_2021_data",
        "AO3_2021_femslash",
        "AO3_2021_overall",
        "AO3_2022_data",
        "AO3_2022_femslash",
        "AO3_2022_overall",
        "AO3_2023_data",
        "AO3_2023_femslash",
        "AO3_2023_overall"
    ]
    filepath = "data/first_clean_up_data/ao3_2013/raw_ao3_2013_overall_ranking.csv"
    result = get_data_set_name(filepath)
    assert result in data_sets_list

def test_returns_correct_data_set_name():
    data_sets = {
        "data/first_clean_up_data/ao3_2013/raw_ao3_2013_overall_ranking.csv":"AO3_2013_overall",
        "data/third_clean_up_data_json_lines_version/ao3_2015/raw_ao3_2015_overall_ranking.json":"AO3_2015_overall",
        "data/second_clean_up_data/ao3_2015/raw_ao3_2015_femslash_ranking.csv":"AO3_2015_femslash",
        "data/fifth_clean_up_data/ao3_2017/stage_5_ao3_2017_data.csv":"AO3_2017_data",
        "data/third_clean_up_data/ao3_2020/raw_ao3_2020_data.json":"AO3_2020_data",
        "data/fourth_clean_up_data/ao3_2022/raw_ao3_2022_femslash_ranking.json":"AO3_2022_femslash",
    }

    for path in data_sets:
        result = get_data_set_name(path)
        assert result == data_sets[path]