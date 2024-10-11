from visualisation.vis_utils.invert_rank import invert_rank
from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_unique_values_list
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df, get_year_df
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

    new_df = pd.DataFrame(data=temp_dict, index=[
        "interracial_ships", 
        "ambiguous_ships", 
        "non-interracial_ships"
    ])
    return new_df


# prep info df with true/false values
def prep_df_for_non_white_ship_comp(ship_info_df:pd.DataFrame):
    """
    takes dataframe that (at least) contains "year", "ship", "fandom", "rank_no", "race_combo" columns

    returns a dict with year keys and dataframe values

    the dataframes contain new columns with true or false/none values based on whether the ship involves
    white, east asian, ambiguous/non-human/unknown characters and whether they're white-involved,
    east asian-involved, non-white, or non-white & non-east asian ships based on that
    """
    new_df = ship_info_df.copy().get(["year", "ship", "fandom", "rank_no", "race_combo"])

    year_dict = {}
    unique_year_list = get_unique_values_list(new_df, "year")
    for year in unique_year_list:

        year_df = get_year_df(new_df, year)
        year_df = year_df.dropna()

        year_df["contains_white_person"] = year_df["race_combo"].str.contains("White|Eu Ind")
            # I want to catch anna and elsa cause they're not a "non-white/non-ea" pairing, that's silly
        year_df["contains_e_asian_person"] = year_df["race_combo"].str.contains("E Asian")
        year_df["contains_ambig_person"] = year_df["race_combo"].str.contains("Ambig")
        year_df["contains_non_human"] = year_df["race_combo"].str.contains("N.H.")
        year_df["contains_unknown"] = year_df["race_combo"].str.contains("Unknown")

        year_df["true"] = True
        year_df["white_involved_ship"] = year_df["true"].where(
            year_df["contains_white_person"] == True
        )
        year_df["e_asian_involved_ship"] = year_df["true"].where(
            year_df["contains_e_asian_person"] == True
        )
        year_df["non_white_ship"] = year_df["true"].where(
            cond= (year_df["contains_white_person"] == False) & (
                year_df["contains_ambig_person"] == False) & (
                year_df["contains_non_human"] == False) & (
                year_df["contains_unknown"] == False)
        )
        year_df["non_white_or_ea_ship"] = year_df["true"].where(
            cond= (year_df["contains_white_person"] == False) & (
                year_df["contains_e_asian_person"] == False) & (
                year_df["contains_ambig_person"] == False) & (
                year_df["contains_non_human"] == False) & (
                year_df["contains_unknown"] == False)
        )
        year_df.pop("true")

        year_dict[int(year)] = year_df

    return year_dict

# how many ships involving {same racial combos as previously} made the wlw ranking each year
def count_non_white_ships(prepped_dict:dict): # should be throwing an error
    """
    takes output from prep_df_for_non_white_ship_comp

    returns a df with numbers for how many ships each year involved white people, involved east 
    asian people, did not involve white people, and did not involve white or east asian people
    """
    concat_list = [prepped_dict[year] for year in prepped_dict]
    new_df = pd.concat(concat_list).get([
        "year", 
        "white_involved_ship", 
        "e_asian_involved_ship", 
        "non_white_ship", 
        "non_white_or_ea_ship"
    ])
    
    new_df = get_label_counts(new_df, "year") # to be seen if "count" will throw an error (probably)
    new_df.pop("count")

    return new_df


# separate out the diff ship info
def separate_out_non_white_ships_info(prepped_dict:dict): # (util)
    """
    takes output from prep_df_for_non_white_ship_comp

    returns a dict with year keys and dict values

    nested dicts contain "white_involved_ship", "e_asian_involved_ship", "non_white_ship", 
    and "non_white_or_ea_ship" keys with dataframe values with "year", "ship", "fandom", 
    "rank_no", "race_combo" & "ship_type"
    """
    year_dict = {}
    lookup_list = [
        "white_involved_ship",
        "e_asian_involved_ship",
        "non_white_ship",
        "non_white_or_ea_ship"
    ]

    for year in prepped_dict:
        year_dict[year] = {}
        year_df = prepped_dict[year]

        for item in lookup_list:
            temp_df = year_df.copy().get(
                ["year", "ship", "fandom", "rank_no", "race_combo", item]
            ).dropna().rename(columns={item: "ship_type"})
            temp_df["ship_type"] = item

            year_dict[year][item] = temp_df

    return year_dict

# top (1-5) ranked ship(s) of “” racial group combos as above each year
def top_non_white_ships(separated_dict:dict):
    """
    takes output from separate_out_non_white_ships_info

    returns a dict with year keys and dataframe values

    the dataframes compile the top 3 (if 3) ships that year for each ship-type: 
    "white_involved_ship", "e_asian_involved_ship", "non_white_ship", "non_white_or_ea_ship"
    """
    new_dict = {}
    lookup_list = [
        "white_involved_ship",
        "e_asian_involved_ship",
        "non_white_ship",
        "non_white_or_ea_ship"
    ]
    for year in separated_dict:
        year_dict = separated_dict[year]
        concat_list = [year_dict[item].head(3) for item in lookup_list]
        new_df = pd.concat(concat_list)
        new_dict[year] = new_df
    
    return new_dict

# average rank of “” racial group combos as above each year vs average white-only & white-involved rank
def average_non_white_ranking(separated_dict:dict):
    """
    takes output from separate_out_non_white_ships_info

    returns a dict with year keys and dataframe values

    the dataframes compile the average rank number that year for each ship-type: 
    "white_involved_ship", "e_asian_involved_ship", "non_white_ship", "non_white_or_ea_ship"
    """
    new_dict = {}
    lookup_list = [
        "white_involved_ship",
        "e_asian_involved_ship",
        "non_white_ship",
        "non_white_or_ea_ship"
    ]
    for year in separated_dict:
        year_dict = separated_dict[year]
        concat_list = [year_dict[item] for item in lookup_list]
        new_df = pd.concat(concat_list)

        new_df["rank_no"] = new_df["rank_no"].apply(invert_rank)
        new_df = new_df.get(
            ["ship_type", "rank_no"]
        ).groupby("ship_type").aggregate("mean").round(2)
        new_df["rank_no"] = new_df["rank_no"].apply(invert_rank)
        new_df["year"] = year
        new_dict[year] = sort_df(new_df, "rank_no", asc=True)
    
    return new_dict
