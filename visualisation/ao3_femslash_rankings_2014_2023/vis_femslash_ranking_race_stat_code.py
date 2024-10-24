from visualisation.vis_utils.invert_rank import invert_rank
from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_unique_values_list
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df, get_year_df
import visualisation.vis_utils.diagram_utils.labels as lbls
import pandas as pd

# character race & race_combo percentages each year
def total_race_nos_by_year(character_info_df:pd.DataFrame, column_name:str): 
    """
    takes dataframe that (at least) contains "year" and "race"/"race_combo" columns

    returns a dict with year keys and dataframe values

    the dataframes contain the numbers of characters of each race/race_combo tag represented that year
    """
    new_df = character_info_df.copy().get(["year", column_name])

    year_dict = {}
    
    unique_year_list = get_unique_values_list(new_df, "year")
    for year in unique_year_list:

        year_df = get_year_df(new_df, year)
        year_df = year_df.dropna()

        counted_df = get_label_counts(year_df, column_name, "year")

        year_dict[int(year)] = sort_df(counted_df, "count")

    return year_dict
