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

        year_df = rename_gender_combos(year_df, column=True) # this should rename the labels first
        year_df = get_label_counts(year_df, "gender_combo", "ship") # then counts them
        year_df = sort_df(year_df, "count")

        year_dict[int(year)] = year_df["count"]

    return year_dict

# def fic_type_by_gender_combo(input_df:pd.DataFrame):
