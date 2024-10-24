from visualisation.vis_utils.make_name_string import make_name_string
from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_unique_values_list,
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df, get_year_df
import pandas as pd
from visualisation.input_data_code.make_file_dfs import make_ships_df

# no 1 hottest character each year (in most ships)
    # & their highest-ranked ship
def hottest_char_ranking(character_info_df:pd.DataFrame, ranking:str):
    """
    takes dataframe that (at least) contains "year", "full_name", "ship", "rank_no", 
    "fandom", "race", "rpf_or_fic" columns

    returns a dict with year keys and dataframe values

    the dataframes contain the numbers of ships each character that year was in,
    ordered from most to least, and which their highest-ranked ship was
    """
    if ranking == "femslash":
        get_list = ["year", "full_name", "ship", "rank_no", "fandom", "race", "rpf_or_fic"]
    else:
        get_list = ["year", "full_name", "ship", "rank_no", "fandom", "race", "gender", "rpf_or_fic"]

    new_df = character_info_df.copy().get(
        get_list
    )

    if ranking != "femslash": # don't need this for femslash
        ships_df = make_ships_df()

    # group by years
    year_dict = {}
    unique_year_list = get_unique_values_list(new_df, "year")
    for year in unique_year_list:
        year_df = get_year_df(new_df, year)
        year_df = year_df.dropna()

        # group by characters
        group_list = get_list[:2] + get_list[4:]
        # count
        hottest_df = get_label_counts(
            year_df, group_list, "ship"
        )
        hottest_df = sort_df(hottest_df, "count")
        hottest_df = hottest_df.reset_index()

        # finding highest ranked ship per character per year
        highest_ships_by_char = {}
        unique_char_list = get_unique_values_list(year_df, "full_name")
        for character in unique_char_list:
            char_df = year_df.where(
                year_df["full_name"] == character
            ).sort_values(by="rank_no").head(1)

            highest_ship = list(char_df["ship"])[0]
            # I wanna attach the gender combo for non-femslash rankings!
            if ranking != "femslash":
                gender_combo = ships_df["gender_combo"].where(
                    (ships_df["slash_ship"] == highest_ship) | (ships_df["gen_ship"] == highest_ship)
                ).dropna()
                gender_combo = list(gender_combo)[0]
            else: gender_combo = ""

            highest_ships_by_char[character] = [highest_ship, gender_combo]
        
        hottest_df["highest_ship"] = [highest_ships_by_char[name][0] for name in hottest_df["full_name"]]
        if ranking != "femslash":
            hottest_df["highest_gender_combo"] = [
                highest_ships_by_char[name][1] for name in hottest_df["full_name"]
            ]
        hottest_df.pop("rank_no")

        year_dict[int(year)] = hottest_df
    
    return year_dict

# need to separate out chars we wanna visualise as a lot are tied & it's by year not fandom
def hottest_char(character_info_df:pd.DataFrame, ranking:str):
    """
    takes dataframe that (at least) contains "year", "full_name", "ship", "rank_no", 
    "fandom", "race", "rpf_or_fic" columns

    returns a dict with year keys and dict values

    each dict contains three keys: "ship_counts", "over_3_ships", and "ranking"

    ship_counts contains a dataframe with how many characters were in each number of ships that year 
    (ie x characters were in y ships)

    over_3_ships contains a dataframe with all characters that were in 3 or more ships that year 
    (including the info columns on highest ranked ship and demo as put out by hottest_char_ranking)

    ranking contains a list of dicts with "no" and "names" keys, whose values represent the number 
    of ships (3+ only) and the names of all characters who tied for that number of ships that year
    """

    hottest_dict = hottest_char_ranking(character_info_df, ranking)

    hottest_data = {}
    for year in hottest_dict:
        hottest_df = hottest_dict[year].copy()

        ship_count_df = hottest_df.copy().get(
            ["highest_ship", "full_name"]
        )
        ship_count_df = get_label_counts(ship_count_df, "highest_ship", "full_name")
        ship_count_df = sort_df(ship_count_df)
        ship_count_df = ship_count_df.reset_index()
        over_3_ships_df = hottest_df.where(hottest_df["count"] > 2).dropna()

        year_ranking = []
        for num in [3,4,5]:
            rank_df = over_3_ships_df.copy().where(over_3_ships_df["count"] == num).dropna()
            if len(rank_df) > 0:
                all_characters = sorted([character for character in rank_df["full_name"]])
                char_string = make_name_string(all_characters)
                year_ranking.append({"no": num, "names": char_string})
        
        hottest_data[year] = {
            "ship_counts": ship_count_df,
            "over_3_ships": over_3_ships_df,
            "ranking": year_ranking
        }

    return hottest_data

