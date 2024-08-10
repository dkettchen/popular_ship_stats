from src.util_functions.attempting_pandas import csv_to_data_frame, json_list_of_dicts_to_data_frame
import pandas as pd

class TestCsv:
    def test_csv_returns_dataframe(self):
        csv_file = "data/second_clean_up_data/ao3_2023/raw_ao3_2023_data.csv"
        #I'm not too worried abt full robustness, bc I know my data has been tested before

        read_df = csv_to_data_frame(csv_file)
        random_df = pd.DataFrame([{"hello": "there"}, {"hello": "and goodbye"}])
        
        assert type(read_df) == type(random_df)

    def test_csv_returns_expected_columns(self):
        csv_file = "data/second_clean_up_data/ao3_2023/raw_ao3_2023_data.csv"
        read_df = csv_to_data_frame(csv_file)
        columns = read_df.columns
        assert list(columns) == ["Rank","Change","Relationship","Fandom","New Works","Total Works","Type","Race"]

    def test_csv_returns_expected_value_types(self):
        csv_file = "data/second_clean_up_data/ao3_2023/raw_ao3_2023_data.csv"
        read_df = csv_to_data_frame(csv_file)
        """
        csv reader only differentiates between str and int, everything else becomes str
        -> no lists etc
        """
        for item in read_df["Rank"]:
            assert type(item) == str
        for item in read_df["Change"]:
            assert type(item) == str
        for item in read_df["Relationship"]:
            assert type(item) == str
            for name in item:
                assert type(name) == str
        for item in read_df["Fandom"]:
            assert type(item) == str
        for item in read_df["New Works"]:
            assert type(item) == int
        for item in read_df["Total Works"]:
            assert type(item) == int
        for item in read_df["Type"]:
            assert type(item) == str
        for item in read_df["Race"]:
            assert type(item) == str

class TestJson:
    def test_json_returns_dataframe(self):
        json_file = "data/third_clean_up_data/ao3_2023/raw_ao3_2023_data.json"
        #I'm not too worried abt full robustness, bc I know my data has been tested before

        read_df = json_list_of_dicts_to_data_frame(json_file)
        random_df = pd.DataFrame([{"hello": "there"}, {"hello": "and goodbye"}])
        
        assert type(read_df) == type(random_df)

    def test_json_returns_expected_columns(self):
        json_file = "data/third_clean_up_data/ao3_2023/raw_ao3_2023_data.json"
        read_df = json_list_of_dicts_to_data_frame(json_file)
        columns = read_df.columns
        assert list(columns) == ["Rank","Change","Relationship","Fandom","New Works","Total Works","Type","Race","Release Date"]

    def test_json_returns_expected_value_types(self):
        json_file = "data/third_clean_up_data/ao3_2023/raw_ao3_2023_data.json"
        read_df = json_list_of_dicts_to_data_frame(json_file)
        for item in read_df["Rank"]:
            assert type(item) == list
            assert type(item[0]) == int
            assert type(item[1]) == str or item[1] == None
        for item in read_df["Change"]:
            assert type(item) == list
            assert type(item[1]) == int or item[1] == None 
                # except apparently in lists it remains none, not nan huh
            assert item[0] in ["+", "-", "New"]
        for item in read_df["Relationship"]:
            assert type(item) == list
            for name in item:
                assert type(name) == str
        for item in read_df["Fandom"]:
            assert type(item) == str
        for item in read_df["New Works"]:
            assert type(item) == int
        for item in read_df["Total Works"]:
            assert type(item) == int
        for item in read_df["Type"]:
            assert type(item) == str or type(item) == list
        for item in read_df["Race"]:
            assert type(item) == list
        # for item in read_df["Release Date"]:
        #     apparently df doesn't return none values?? only smth called nan but of type float??

        second_file = "data/third_clean_up_data/ao3_2015/raw_ao3_2015_femslash_ranking.json"
        second_df = json_list_of_dicts_to_data_frame(second_file)
        # for item in second_df["New Works"]:
        #     ok this also returns nan instead of null, got it
        for item in second_df["Release Date"]:
            assert type(item) == str # I guess dates were strings, which is fine for now anyway


