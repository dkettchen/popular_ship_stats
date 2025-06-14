from src.cleaning_code_refactor_utils.find_paths import find_paths
from data.reference_and_test_files.refactor_helper_files.folder_lookup import CLEAN_FOLDER
from re import split
import pandas as pd

def read_rankings(end_year:int, start_year:int=2013, which_ranking:str="all", website:str="AO3"):
    """
    returns a nested dict (by year and then ranking) with dfs for each qualifying ranking file 
    based on the requested criteria
    ex. if requested year range is 2013 to 2016, only data from those years will be returned

    currently available years are 
    2013, 2014, 2015, 2016, 2017, 2019, 2020, 2021, 2022, 2023, 2024

    currently ranking can be "all", "annual", "overall" or "femslash" 
    and will only return the requested ranking(s)

    currently we only have AO3 data
    """

    # we're inherently only requesting one website for now 
    # as I don't think it'll be useful to put both into one file
    all_paths = [path for path in find_paths(CLEAN_FOLDER) if website in path]

    # get all years we're looking for
    all_years = [year for year in range(start_year, end_year + 1, 1)]
    
    # sorting by ranking if requested
    if which_ranking != "all":
        ranking_paths = [path for path in all_paths if which_ranking in path]
    else:
        ranking_paths = all_paths
    
    df_dict = {year:{} for year in all_years}
    # sorting for requested years
    for filepath in ranking_paths:
        # retrieve year from filepath
        split_path = split("_",filepath) # .../{website}_{year}_{ranking}.csv
        year = int(split_path[-2])
        ranking = split_path[-1][:-4]

        # then check against years list
        if year in all_years:
            # read in data
            df = pd.read_csv(filepath)

            # add df data on ranking key
            df_dict[year][ranking] = df

    return df_dict
    