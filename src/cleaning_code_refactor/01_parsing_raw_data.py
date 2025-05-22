from src.cleaning_code_refactor_utils.find_paths import find_paths
from src.cleaning_code_refactor_utils.read_txt import read_txt
from src.cleaning_code_refactor_utils.split_values import split_data
import pandas as pd

files = find_paths("data/raw_data")

# removing non-ranking filepaths
filepaths = [path for path in files if "2013_overall" in path or "2013" not in path]

for filepath in filepaths:
    # read in data
    read_data = read_txt(filepath)

    # retrieving year & ranking from filepath
    year = int(filepath[31:35])
    ranking = filepath[36:-4]
    if "ranking" in ranking:
        ranking = ranking[:-8]
    if "2019_" in ranking:
        year = 2019
        ranking = ranking[5:]

    # separate all values
    split_list = split_data(read_data, year, ranking)

    # turn into df
    df = pd.DataFrame(split_list[1:], columns=split_list[0])

    # escape apostrophes

    # generate folders along with files
    # print to csv files



    # file_path = "data/first_clean_up_data/" + path[14:-4] + ".csv"
    # final_list = escape_apostrophes(new_list)
    # make_csv_file(final_list, file_path)
