from visualisation.vis_utils.read_csv_to_df import df_from_csv

def make_femslash_dfs():
    """
    returns a dictionary with year keys and dataframe values

    each dataframe is the corresponding year's ao3 femslash ranking data as read 
    from the data/fifth_clean_up_data/ folder
    """
    years = [2014,2015,2016,2017,2019,2020,2021,2022,2023]

    femslash_df_dict = {}
    for year in years:
        filepath = f"data/fifth_clean_up_data/ao3_{year}/stage_5_ao3_{year}_femslash.csv"
        femslash_df_dict[year] = df_from_csv(filepath)

    return femslash_df_dict

def make_characters_df():
    """
    returns a dataframe with the read data from data/fifth_clean_up_data/stage_5_characters.csv
    """
    df = df_from_csv("data/fifth_clean_up_data/stage_5_characters.csv")
    return df

def make_ships_df():
    """
    returns a dataframe with the read data from data/fifth_clean_up_data/stage_5_ships.csv
    """
    df = df_from_csv("data/fifth_clean_up_data/stage_5_ships.csv")
    return df

def make_yearly_df_dict(ranking:str):
    """
    returns a dictionary with year keys and dataframe values

    each dataframe is the corresponding year's (currently implemented:) 
    ao3 ranking data as read from the data/fifth_clean_up_data/ folder

    - for femslash ranking: ranking="femslash"
    - for overall ranking: ranking="overall"
    - for annual ranking: ranking="annual"
    """
    if ranking == "femslash":
        years = [2014,2015,2016,2017,2019,2020,2021,2022,2023]
    elif ranking == "overall":
        years = [2013,2014,2015,2016,2017,2019,2020,2021,2022,2023]
    elif ranking == "annual":
        years = [2016,2017,2019,2020,2021,2022,2023]
        ranking = "data"

    df_dict = {}
    for year in years:
        filepath = f"data/fifth_clean_up_data/ao3_{year}/stage_5_ao3_{year}_{ranking}.csv"
        df_dict[year] = df_from_csv(filepath)

    return df_dict