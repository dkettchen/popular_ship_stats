from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_unique_values_list,
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df, get_year_df
from copy import deepcopy
import pandas as pd
import visualisation.vis_utils.diagram_utils.ranks as ranks

# top ships & their demo each year
def top_ships(ship_info_df:pd.DataFrame, ranking:str):
    """
    takes a dataframe that contains (at least) "year", "ship", "fandom", "race_combo", and "rpf_or_fic" 
    columns and is sorted by ranks already

    if the ranking is not femslash, it also needs to contain "gender_combo"

    if the ranking is femslash, it returns the top 5 ships, otherwise it returns the top 10

    returns a dictionary with year keys and dataframe values, of the top ships in that year
    """
    if ranking == "femslash":
        get_list = ["year", "ship", "fandom", "race_combo", "rpf_or_fic"]
        # leaving out gender combo cause all of em seem to be F / F
    else:
        get_list = ["year", "ship", "fandom", "gender_combo", "race_combo", "rpf_or_fic"]

    new_df = ship_info_df.copy().get(get_list)

    if ranking == "femslash":
        number = 5
    else: number = 10

    year_dict = {}
    unique_year_list = get_unique_values_list(new_df, "year")
    for year in unique_year_list:
        year_df = get_year_df(new_df, year)
        year_df = year_df.dropna().head(number)
        year_dict[int(year)] = year_df
    
    return year_dict


def make_concat_df(input_dict:dict): # helper
    """
    concatenates all values of a dictionary with dataframe values into one big dataframe
    """
    all_year_dfs = list(input_dict.values())
    complete_df = pd.concat(all_year_dfs)

    return complete_df


def count_appearances(top_ships:dict, ranking:str):
    """
    takes output from top_ships

    returns a dataframe with the count of number of appearances of each ship in the top ships
    """
    new_df = make_concat_df(top_ships)

    if ranking == "femslash":
        index_list = ["ship", "fandom", "race_combo", "rpf_or_fic"]
    else: index_list = ["ship", "fandom", "gender_combo", "race_combo", "rpf_or_fic"]

    most_appearances = get_label_counts(new_df, index_list, "year")
    most_appearances = sort_df(most_appearances, "count")

    return most_appearances.reset_index().rename(columns={"count": "no_of_appearances"})

def count_streaks(top_ships:dict):
    """
    takes output from top_ships

    returns a dataframe with the longest streak of each ship in the top ships
    """
    all_top_ships = make_concat_df(top_ships)

    # set counters for each pairing (to zero)
    counter_dict = {
        ship : 0 for ship in sorted(list(set(all_top_ships["ship"])))
    }

    # set up streak storage
    streak_storage = deepcopy(counter_dict)
    for ship in streak_storage:
        streak_storage[ship] = []

    # go through years in order
    all_years = sorted(list(top_ships.keys()))
    for year in all_years:

        for ship in counter_dict:
            if ship in list(top_ships[year]["ship"]):
                counter_dict[ship] += 1 # increase streak
                streak_storage[ship].append(counter_dict[ship]) # add counter to storage
            else: # if ship isn't in top ships that year
                counter_dict[ship] = 0 # reset counter to zero

    final_ranking = {}
    # get each pairing's longest streak number    
    for ship in streak_storage:
        longest_streak = sorted(streak_storage[ship], reverse=True)[0]
        final_ranking[ship] = longest_streak

    new_df = pd.DataFrame(
        data=final_ranking.values(), 
        index=final_ranking.keys(), 
        columns=["longest_streak"]
    )
    new_df = sort_df(new_df, "longest_streak")

    return new_df.reset_index().rename(columns={"index": "ship"})


# longest running top ship (longest streak & most appearances)
def longest_running_top_ships(appearances:pd.DataFrame, streaks:pd.DataFrame, ranking:str):
    """
    takes the output of count_appearances and count_streaks

    returns a dataframe with the top 5 ships for most appearances and longest streak, 
    including their respective numbers
    """
    if ranking == "femslash":
        number = 5
        rank_nos = ranks.top_10_list[:5]
    else: 
        number = 10
        rank_nos = ranks.top_10_list

    top_5_for_appearances = appearances.head(number)
    top_5_for_streaks = streaks.head(number)
    
    rank_dict = {
        "top_ships_by_appearances": top_5_for_appearances["ship"].values,
        "no_of_appearances": top_5_for_appearances["no_of_appearances"].values,
        "top_ships_by_streak": top_5_for_streaks["ship"].values,
        "longest_streak": top_5_for_streaks["longest_streak"].values
    }
    new_df = pd.DataFrame(index=rank_nos, data=rank_dict)

    return new_df

