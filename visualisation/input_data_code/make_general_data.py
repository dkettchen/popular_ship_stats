import pandas as pd
from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_unique_values_list,
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df, get_year_df
from visualisation.vis_utils.rename_gender_combos import rename_gender_combos
from visualisation.vis_utils.sort_race_combos import sort_race_combos
from visualisation.input_data_code.get_data_df import get_data_df

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

    returns a dict with df values containing the number of rpf and fictional ships that year
    """

    new_df = input_df.copy()

    year_dict = {}
    unique_year_list = get_unique_values_list(new_df, "year")
    for year in unique_year_list:
        year_df = get_year_df(new_df, year)

        year_df = get_data_df(year_df, "rpf", "overall")
        
        year_dict[int(year)] = year_df.rename(columns={"count":"no_of_ships"})

    return year_dict


def get_counts(input_df:pd.DataFrame, column_name:str, count_column:str):
    """
    takes a ship_info_df

    returns a dict with series values containing the numbers of (count_column) 
    by (column_name) that year
    """

    new_df = input_df.copy()

    year_dict = {}
    unique_year_list = get_unique_values_list(new_df, "year")
    for year in unique_year_list:
        year_df = get_year_df(new_df, year)

        if column_name == ["gender_combo", "race_combo"]: # renaming combos!
            year_df = rename_gender_combos(year_df, column=True)
            renaming_dict = sort_race_combos(year_df["race_combo"]) 
            year_df["race_combo"] = [renaming_dict[combo] if combo in renaming_dict else combo for combo in year_df["race_combo"]]

        year_df = get_label_counts(year_df, column_name, count_column)
        if column_name in [
            ["gender", "race"],
            ["gender_combo", "race_combo"]
        ]:
            year_df = sort_df(year_df) # sorting by multi index
        else:
            year_df = sort_df(year_df, "count") # sorting by values

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

    return year_dict
