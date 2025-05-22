import pandas as pd
from src.cleaning_code_refactor_utils.find_paths import find_paths
from src.cleaning_code_refactor_utils.read_txt import read_txt
from src.cleaning_code_refactor_utils.split_values import split_data
from src.cleaning_code_refactor_utils.escape_apostrophes import escape_apostrophes
from src.cleaning_code_refactor_utils.remove_commas import remove_commas
from src.cleaning_code_refactor_utils.remove_equals import remove_equals
from src.cleaning_code_refactor_utils.separate_change_symbols import separate_change_symbol
from src.cleaning_code_refactor_utils.add_white_white_lists import add_white_white_list

def parse_txt():
    """
    reads in all the files in data/raw_data (currently only expecting ao3 data)

    separates the text into the appropriate columns and values, 
    and adds empty columns where missing

    returns a nested dict containing all the parsed tables as dfs categorised by year and ranking

    output_dict[year][ranking] -> df
    """

    files = find_paths("data/raw_data")

    # removing non-ranking filepaths
    filepaths = [path for path in files if "2013_overall" in path or "2013" not in path]

    df_dict = {}

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

        # add list for white/white pairings
        if "Race" in df.columns:
            df["Race"] = df["Race"].apply(add_white_white_list)

        # add missing columns with empty or relevant values
        missing_columns = {
            "Change" : [None, None],
            "New Works" : None,
            "Type" : ["F", "F"], # only missing in femslash (we'll fix the included genderqueers later)
            "Race" : [None, None],
            "Release Date" : None
        }
        for column in missing_columns.keys():
            if column not in df.columns:
                if type(missing_columns[column]) != list:
                    df[column] = missing_columns[column]
                else:
                    df[column] = [missing_columns[column] for i in range(len(df))]
        
        if year not in df_dict.keys():
            df_dict[year] = {}
        df_dict[year][ranking] = df

    return df_dict

if __name__ == "__main__":
    parse_txt()