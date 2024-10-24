from visualisation.vis_utils.invert_rank import invert_rank
from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_unique_values_list
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df, get_year_df
import visualisation.vis_utils.diagram_utils.labels as lbls
import pandas as pd


# how many multiracial characters each year
def total_multi_nos_by_year(input_dict:dict, column_name:str):
    """
    takes output dict from total_race_nos_by_year & a column name ("race" or "race_combo")

    returns a dataframe with the total no of multiracial and non-multiracial characters 
    or ships containing or not containing multiracial characters per year
    """
    temp_dict = {}
    for year in input_dict:
        df = input_dict[year].copy().reset_index()

        total = df["count"].sum()
        multi = df.where(
            df[column_name].str.contains("(Multi)", regex=False) # regex false suppressed the warning!
        )["count"].sum()
        non_multi = total - multi

        temp_dict[year] = [multi, non_multi]

    if column_name == "race":
        index_list = ["multi_chars", "non-multi_chars"]
    elif column_name == "race_combo":
        index_list = ["with_multi_chars", "without_multi_chars"]

    new_df = pd.DataFrame(data=temp_dict, index=index_list)
    return new_df

# race_combos of which how many interracial vs same
def total_interracial_ratio(race_combo_percent:dict):
    """
    takes output dict from total_race_nos_by_year ("race_combo" version)

    returns a dataframe with the total no of interracial and non-interracial ships per year
    """
    temp_dict = {}
    for year in race_combo_percent:
        df = race_combo_percent[year].copy().reset_index()

        total = df["count"].sum()
        inter = df.where(
            (df["race_combo"].str.contains("/")) & (df["race_combo"].str.contains("Ambig") == False)
        )["count"].sum()
        ambig = df.where(
            df["race_combo"].str.contains("Ambig")
        )["count"].sum()
        non_inter = total - inter - ambig

        temp_dict[year] = [inter, ambig, non_inter]

    new_df = pd.DataFrame(data=temp_dict, index=lbls.interracial_categories)
    return new_df


# how many racial groups each year
def total_racial_groups(race_percent:dict):
    """
    takes output dict from total_race_nos_by_year ("race" version)

    returns a series with the total no of racial groups represented each year
    """
    temp_dict = {}
    for year in race_percent:
        df = race_percent[year].copy().reset_index()
        total = df["count"].count()
        temp_dict[year] = total
    new_srs = pd.Series(data=temp_dict)
    return new_srs

