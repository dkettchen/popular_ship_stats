from src.cleaning_code_refactor_utils.find_paths import find_paths
from src.cleaning_code_refactor_utils.read_txt import read_txt
from src.cleaning_code_refactor_utils.split_values import split_data
import pandas as pd
from src.cleaning_code_refactor_utils.escape_apostrophes import escape_apostrophes
from src.cleaning_code_refactor_utils.remove_commas import remove_commas
from src.cleaning_code_refactor_utils.remove_equals import remove_equals
from src.cleaning_code_refactor_utils.separate_change_symbols import separate_change_symbol

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

    ## first stage cleaning

    # separate all values
    split_list = split_data(read_data, year, ranking)

    # turn into df
    df = pd.DataFrame(split_list[1:], columns=split_list[0])
    
    ## I moved renaming up here already for ease of column calling
    # rename columns
    renaming_dict = {
        "#": "Rank",
        "New": "Change",
        "Pairing Tag": "Relationship",
        "Pairing": "Relationship",
        "Ship": "Relationship",
        "Works": "Total Works",
        "Total": "Total Works",
        "Fics": "Total Works",
    }
    df = df.rename(columns=renaming_dict)

    # escape apostrophes (replace all apostrophes & quotes with ')
    df["Fandom"] = df["Fandom"].apply(escape_apostrophes)
    def iterate_and_escape(string_list:list[str]):
        """
        iterate over list of strings and run escape apostrophes on each string
        """
        new_list = []
        for s in string_list:
            new_s = escape_apostrophes(s)
            new_list.append(new_s)
        return new_list
    df["Relationship"] = df["Relationship"].apply(iterate_and_escape)

    ## second stage cleaning

    # remove commas from works numbers
    if year in [2015, 2016]:
        for column in ["New Works", "Total Works"]:
            if column in df.columns:
                df[column] = df[column].apply(remove_commas)

    # remove = from ranks
    df["Rank"] = df["Rank"].apply(remove_equals)

    # separate change symbols
    if year != 2013 \
    and not (year == 2014 and ranking == "femslash") \
    and not (year == 2016 and ranking == "data"):
        df["Change"] = df["Change"].apply(separate_change_symbol)

    ## third stage cleaning




    # generate filepath

    # generate folders along with files
    # print to csv files with ` as escape char


