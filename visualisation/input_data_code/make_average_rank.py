import pandas as pd
from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_unique_values_list,
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df, get_year_df
from visualisation.vis_utils.rename_gender_combos import rename_gender_combos


# possibly refactor to unite with average_non_white_ranking?
def average_rank(input_df:pd.DataFrame, column_name:str):
    """
    takes dataframe

    returns average rank per: 
    - column_name="gender" (character df)
    - column_name="gender_combo" (ship df)
    """

    new_df = input_df.copy()
    if column_name == "gender_combo": 
        # renaming labels first
        new_df = rename_gender_combos(new_df, column=True) 

    # prepping df
    index_list = sorted(get_unique_values_list(new_df, column_name))
    unique_year_list = get_unique_values_list(new_df, "year")
    average_df = pd.DataFrame(
        index=index_list,
        columns=[str(int(year)) for year in unique_year_list]
    )

    # collecting yearly averages for each label
    for year in unique_year_list:
        year_df = get_year_df(new_df, year)
        values = year_df.groupby(column_name)["rank_no"].agg("mean").round(2)
        average_df[str(int(year))] = values
    
    # adding total average
    all_time_average = [float(round(average_df.loc[item].agg("mean"), 2)) for item in index_list]
    average_df["total"] = all_time_average

    average_df = average_df.fillna("N/A")

    return average_df

