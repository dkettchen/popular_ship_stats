from src.util_functions.retrieve_data_from_csv import read_data_from_csv
from src.util_functions.write_csv_file import make_csv_file
import pandas as pd

def prep_canon_and_incest_data_file():
    # read from ships file
    read_data = read_data_from_csv("data/fifth_clean_up_data/stage_5_ships.csv")

    # only get slash_ship and fandom columns
    new_data = []
    for row in read_data:
        new_row = [row[0], row[3]]
        new_data.append(new_row)

    # print to new file
    make_csv_file(new_data, "data/reference_and_test_files/additional_data/additional_ship_data.csv")

    # -> then I can manually add canon & relationships info

if __name__ == "__main__":
    prep_canon_and_incest_data_file()