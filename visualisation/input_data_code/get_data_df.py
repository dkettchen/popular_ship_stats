from visualisation.vis_utils.sort_race_combos import sort_race_combos
from visualisation.vis_utils.df_utils.retrieve_numbers import get_label_counts, sum_label_nums
from visualisation.vis_utils.df_utils.make_dfs import sort_df
import pandas as pd

def get_data_df(input_df:pd.DataFrame, data_case:str):
    """
    takes output from (currently implemented:)
    - df_from_csv("data/fifth_clean_up_data/stage_5_ships.csv") and returns
        - total number of ships in file (data_case="total_ships")
        - total number of ships of each gender combo (data_case="total_gender_combos")
        - fandom, slash_ship, gender_combo, and race_combo columns (data_case="ships_per_fandom_util")
        - number of ships per fandom (data_case="ships_per_fandom")
        - total number of ships of each race combo (data_case="total_race_combos")
        - number of rpf and non-rpf ships (data_case="rpf")
    - df_from_csv("data/fifth_clean_up_data/stage_5_characters.csv") and returns
        - total number of characters in file (data_case="total_chars")
        - total number of characters of each gender tag 
        in custom order to be visualised (data_case="total_genders")
        - total number of characters of each race tag (data_case="total_racial_groups")
        - number of racial groups in each fandom (data_case="racial_diversity")
    
    as a dataframe
    """
    # making input case insensitive
    data_case = data_case.lower()

    # making lookup dicts
    column_lookup = {
        "total_ships": ["slash_ship"],
        "total_gender_combos": ["slash_ship","gender_combo"],
        "ships_per_fandom_util": ["fandom", "slash_ship", "gender_combo", "race_combo"],
        "ships_per_fandom": ["fandom", "slash_ship", "gender_combo", "race_combo"],
        "total_race_combos": ["slash_ship","race_combo"],
        "rpf": ["slash_ship", "rpf_or_fic"],
        "total_chars": ["full_name"],
        "total_genders": ["full_name","gender"],
        "total_racial_groups": ["full_name","race"],
        "racial_diversity": ["full_name","fandom","race"],
    }
    index_names_lookup = {
        "total_ships": {"slash_ship":"total_num_of_ships"}, 
        "total_chars": {"full_name":"total_num_of_characters"},
        "total_gender_combos": {
            "F / M": "M / F",
            "Ambig / M": "M / Ambig",
            "Ambig / F": "F / Ambig",
            "M | Other / M": "M / M | Other"
        }
    }

    new_df = input_df.copy()
    new_df = new_df.get(column_lookup[data_case]) # getting relevant columns via lookup dict

    # setting group_column & count_column for get_label_counts
    if data_case in ["total_gender_combos", "ships_per_fandom", "total_race_combos", "rpf"]:
        count_column = "slash_ship"
        if data_case == "total_gender_combos":
            group_column = "gender_combo"
        elif data_case == "ships_per_fandom":
            group_column = "fandom"
        elif data_case == "total_race_combos":
            group_column = "race_combo"
        elif data_case == "rpf":
            group_column = "rpf_or_fic"
    elif data_case in ["total_genders", "total_racial_groups", "racial_diversity"]:
        count_column = "full_name"
        if data_case == "total_genders":
            group_column = "gender"
        elif data_case == "total_racial_groups":
            group_column = "race"
        elif data_case == "racial_diversity":
            group_column = ["fandom", "race"]

    # counting
    if data_case in ["total_ships", "total_chars"]: # just using .count()
        new_df = new_df.count()
    elif data_case in [ # using get_label_counts util
        "total_gender_combos",
        "ships_per_fandom", 
        "total_race_combos", 
        "rpf", 
        "total_genders", 
        "total_racial_groups", 
        "racial_diversity"
    ]:
        counted_df = get_label_counts(new_df, group_column, count_column)
        if data_case != "ships_per_fandom":
            new_df = counted_df

    # renaming indexes
    if data_case in ["total_ships", "total_chars", "total_gender_combos"]: # using lookup dict
        new_df = new_df.rename(index=index_names_lookup[data_case])
    elif data_case == "total_race_combos": # using custom index_names
        unique_combos = sorted(list(set(new_df.index)))
        index_names = sort_race_combos(unique_combos)
        new_df = new_df.rename(index=index_names)

    # summing label nums by index
    if data_case in ["total_gender_combos", "total_race_combos"]:
        new_df = sum_label_nums(new_df, "index")

    # sorting by count column
    if data_case in ["total_race_combos", "total_racial_groups"]:
        new_df = sort_df(new_df, "count")
    elif data_case == "total_gender_combos": # ascending
        new_df = sort_df(new_df, "count", asc=True) # asc??

    # any other custom bits
    if data_case == "ships_per_fandom":
        new_df = new_df.join(
            other=counted_df["count"], 
            on=new_df.fandom, 
            how="inner", 
        )
        column_names = {"count": "total_ships"}
        new_df = new_df.rename(columns=column_names)
        new_df.pop("key_0")
    elif data_case == "total_genders":
        new_df.index = pd.Categorical( # to set a custom order!
            new_df.index, 
            [
                "M | Other",
                "F | Other",
                "F",
                "Other",
                "M | F | Other",
                "Ambig",
                "M",
            ]
        )
        new_df = new_df.sort_index()
    elif data_case == "racial_diversity":
        new_df = pd.DataFrame(
            index=new_df.index,
            columns=["count"],
            data=new_df
        )

    return new_df