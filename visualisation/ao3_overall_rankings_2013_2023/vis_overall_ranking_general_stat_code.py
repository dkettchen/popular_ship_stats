import pandas as pd
from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_unique_values_list,
    sum_label_nums
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df, get_year_df
from visualisation.vis_utils.rename_gender_combos import rename_gender_combos

def get_fic_type(input_df:pd.DataFrame):
    """
    takes a ship_info_df

    returns a dict with series values containing the number of gen and slash ships that year
    """

    new_df = input_df.copy()

    year_dict = {}
    unique_year_list = get_unique_values_list(new_df, "year")
    for year in unique_year_list:
        year_df = get_year_df(new_df, year)
        year_df = get_label_counts(year_df, "fic_type", "ship")
        year_df = sort_df(year_df, "count")
        year_dict[int(year)] = year_df["count"]

    return year_dict

def get_gender_combos(input_df:pd.DataFrame):
    """
    takes a ship_info_df

    returns a dict with series values containing the number of each ship type that year
    """

    new_df = input_df.copy()

    year_dict = {}
    unique_year_list = get_unique_values_list(new_df, "year")
    for year in unique_year_list:
        year_df = get_year_df(new_df, year)

        # this may be able to be implemented as a data_case in 
        # get_data_df(data_case="total_gender_combos") instead 
        # (currently uses "slash_ship" instead of "ship" -> would need to be adjusted
        # also asc -> I don't think it needs to be asc)
        year_df = get_label_counts(year_df, "gender_combo", "ship")
        year_df = rename_gender_combos(year_df)
        year_df = sum_label_nums(year_df, "index")
        year_df = sort_df(year_df, "count")

        year_dict[int(year)] = year_df["count"]

    return year_dict