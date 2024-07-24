from src.second_cleaning_stage_code.clean_all_number_values import remove_commas_from_2015_2016_fics_tallies
from src.util_functions.retrieve_data_from_csv import read_data_from_csv

class TestRemoveCommas:
    def test_does_not_mutate_input_list(self):
        remove_commas_from_2015_2016_fics_tallies(
            read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")
        )
        pass
    #TODO: implement test suite pls, very robust n stuff