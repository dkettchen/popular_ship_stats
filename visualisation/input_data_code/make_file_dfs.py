from visualisation.vis_utils.read_csv_to_df import df_from_csv

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

def make_yearly_df_dict(ranking:str, end_date:int):
    """
    returns a dictionary with year keys and dataframe values

    each dataframe is the corresponding year's (currently implemented:) 
    ao3 ranking data as read from the data/fifth_clean_up_data/ folder

    - for femslash ranking: ranking="femslash"
    - for overall ranking: ranking="overall"
    - for annual ranking: ranking="annual"
    """
    # adding years until 2017 (when it skipped 2018)
    if ranking == "femslash":
        years = [2014,2015,2016,2017]
    elif ranking == "overall":
        years = [2013,2014,2015,2016,2017]
    elif ranking == "annual":
        years = [2016,2017]
        ranking = "data"

    # adding remaining years
    additional_years_needed = end_date - 2018 # the missing year we're excluding
    # if 2023: 5
    # if 2024: 6
    # etc

    additional_years_available = []
    current_year = 2018
    for _ in range(additional_years_needed):
        current_year += 1
        additional_years_available.append(current_year)

    years += additional_years_available

    # making dict
    df_dict = {}
    for year in years:
        filepath = f"data/fifth_clean_up_data/ao3_{year}/stage_5_ao3_{year}_{ranking}.csv"
        df_dict[year] = df_from_csv(filepath)

    return df_dict