import pandas as pd
from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_unique_values_list,
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df, get_year_df
from visualisation.vis_utils.rename_gender_combos import rename_gender_combos
from visualisation.input_data_code.get_data_df import get_data_df

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

    returns a dict with series values containing the number of each gender combo that year
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

def get_rpf(input_df:pd.DataFrame):
    """
    takes a ship_info_df

    returns a dict with series values containing the number of rpf and fictional ships that year
    """

    new_df = input_df.copy()

    year_dict = {}
    unique_year_list = get_unique_values_list(new_df, "year")
    for year in unique_year_list:
        year_df = get_year_df(new_df, year)

        year_df = get_data_df(year_df, "rpf", "overall")
        
        year_dict[int(year)] = year_df["count"]

    return year_dict


def get_by_gender_combo(input_df:pd.DataFrame, column_name:str):
    """
    takes a ship_info_df

    returns a dict with series values containing the number of input column_name 
    (currently implemented: "fic_type", "rpf_or_fic") for each gender combo that year
    """
    new_df = input_df.copy()

    year_dict = {}
    unique_year_list = get_unique_values_list(new_df, "year")
    for year in unique_year_list:
        year_df = get_year_df(new_df, year)

        year_df = rename_gender_combos(year_df, column=True) # this should rename the labels first
        year_df = get_label_counts(year_df, [column_name, "gender_combo"], "ship") # then counts them
        year_df = sort_df(year_df)

        year_dict[int(year)] = year_df["count"]

    print(year_dict)
    return year_dict
